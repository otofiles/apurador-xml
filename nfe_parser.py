import os
import re
import threading
import zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal, InvalidOperation

LOCAL_TAG = re.compile(r"^\{[^}]+\}(.+)$")


def _name(tag: str) -> str:
    m = LOCAL_TAG.match(tag)
    return m.group(1) if m else tag


def _child(parent, name: str):
    for c in list(parent):
        if _name(c.tag) == name:
            return c
    return None


def _text(parent, name: str) -> str:
    c = _child(parent, name)
    if c is None or c.text is None:
        return ""
    return c.text.strip()


class Documento:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.chave = ""
        self.modelo = 0
        self.modelo_nome = "NF-e"
        self.numero = ""
        self.serie = ""
        self.emissao = ""
        self.emitente = ""
        self.valor = None
        self.vBC = None
        self.vICMS = None
        self.vICMSDeson = None
        self.vFCP = None
        self.vBCST = None
        self.vST = None
        self.vFCPST = None
        self.vFCPSTRet = None
        self.vProd = None
        self.vFrete = None
        self.vSeg = None
        self.vDesc = None
        self.vII = None
        self.vIPI = None
        self.vIPIDevol = None
        self.vPIS = None
        self.vCOFINS = None
        self.vOutro = None
        self.vTotTrib = None
        self.vBCIBSCBS = None
        self.vIBSUF = None
        self.vIBSMun = None
        self.vIBS = None
        self.vCredPresIBS = None
        self.vCBS = None
        self.vCredPresCBS = None
        self.vIBSMono = None
        self.vCBSMono = None
        self.vIBSMonoReten = None
        self.vCBSMonoReten = None
        self.vIBSMonoRet = None
        self.vCBSMonoRet = None
        self.vNFTot = None
        self.status = ""
        self.erro = ""
        self.evento_cancelamento = False
        self.evento = False


STATUS_AUTORIZADA = "Autorizada"
STATUS_CANCELADA = "Cancelada"
STATUS_DENEGADA = "Denegada"
STATUS_SEM_PROTOCOLO = "Sem protocolo"
STATUS_REJEITADA = "Rejeitada"
STATUS_INVALIDA = "Inválida"
STATUS_CANCELAMENTO = "Cancelamento"
STATUS_INUTILIZADA = "Inutilizada"
STATUS_CCE = "Evento CC-e"
STATUS_EVENTO = "Evento"

STATUS_ORDEM = [
    STATUS_AUTORIZADA,
    STATUS_REJEITADA,
    STATUS_DENEGADA,
    STATUS_CANCELADA,
    STATUS_SEM_PROTOCOLO,
    STATUS_INUTILIZADA,
    STATUS_CANCELAMENTO,
    STATUS_CCE,
    STATUS_EVENTO,
    STATUS_INVALIDA,
]

TRIBUTOS = [
    ("vBC", "BC ICMS", 90),
    ("vICMS", "ICMS", 90),
    ("vICMSDeson", "ICMS Deson.", 95),
    ("vFCP", "FCP", 80),
    ("vBCST", "BC ICMS ST", 95),
    ("vST", "ICMS ST", 90),
    ("vFCPST", "FCP ST", 80),
    ("vFCPSTRet", "FCP ST Ret", 95),
    ("vProd", "Produtos", 100),
    ("vFrete", "Frete", 80),
    ("vSeg", "Seguro", 80),
    ("vDesc", "Desconto", 90),
    ("vII", "Imp. Import.", 90),
    ("vIPI", "IPI", 80),
    ("vIPIDevol", "IPI Devol.", 95),
    ("vPIS", "PIS", 80),
    ("vCOFINS", "COFINS", 90),
    ("vOutro", "Outras", 80),
    ("vTotTrib", "Total Tributos", 110),
    ("vBCIBSCBS", "BC IBS/CBS", 100),
    ("vIBSUF", "IBS UF", 90),
    ("vIBSMun", "IBS Mun", 90),
    ("vIBS", "IBS Total", 90),
    ("vCredPresIBS", "Cred Pres IBS", 110),
    ("vCBS", "CBS", 90),
    ("vCredPresCBS", "Cred Pres CBS", 110),
    ("vIBSMono", "IBS Mono", 90),
    ("vCBSMono", "CBS Mono", 90),
    ("vIBSMonoReten", "IBS Mono Reten", 110),
    ("vCBSMonoReten", "CBS Mono Reten", 110),
    ("vIBSMonoRet", "IBS Mono Ret", 110),
    ("vCBSMonoRet", "CBS Mono Ret", 110),
    ("vNFTot", "Total NF (vNFTot)", 120),
]

CSTAT_DENEGADOS = {"110", "301", "302", "303"}
CSTAT_INUTILIZADA = {"135", "136"}


def _parse_valor(texto: str):
    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        return Decimal(texto)
    except InvalidOperation:
        return None


def _parse_inf_nfe(inf_nfe, arquivo):
    doc = Documento(arquivo)

    _id = inf_nfe.attrib.get("Id", "")
    if _id.startswith("NFe"):
        doc.chave = _id[3:]
    elif len(_id) == 44:
        doc.chave = _id

    ide = _child(inf_nfe, "ide")
    if ide is not None:
        try:
            doc.modelo = int(_text(ide, "mod") or "0")
        except ValueError:
            doc.modelo = 0
        doc.numero = _text(ide, "nNF")
        doc.serie = _text(ide, "serie")
        doc.emissao = _text(ide, "dhEmi") or _text(ide, "dEmi")
    doc.modelo_nome = "NFC-e" if doc.modelo == 65 else "NF-e"

    emit = _child(inf_nfe, "emit")
    if emit is not None:
        nome = _text(emit, "xNome")
        cnpj = _text(emit, "CNPJ") or _text(emit, "CPF")
        doc.emitente = nome
        if cnpj:
            doc.emitente = (nome + " " + cnpj).strip() if nome else cnpj

    total = _child(inf_nfe, "total")
    if total is not None:
        icms = _child(total, "ICMSTot")
        if icms is not None:
            doc.valor = _parse_valor(_text(icms, "vNF"))
            doc.vBC = _parse_valor(_text(icms, "vBC"))
            doc.vICMS = _parse_valor(_text(icms, "vICMS"))
            doc.vICMSDeson = _parse_valor(_text(icms, "vICMSDeson"))
            doc.vFCP = _parse_valor(_text(icms, "vFCP"))
            doc.vBCST = _parse_valor(_text(icms, "vBCST"))
            doc.vST = _parse_valor(_text(icms, "vST"))
            doc.vFCPST = _parse_valor(_text(icms, "vFCPST"))
            doc.vFCPSTRet = _parse_valor(_text(icms, "vFCPSTRet"))
            doc.vProd = _parse_valor(_text(icms, "vProd"))
            doc.vFrete = _parse_valor(_text(icms, "vFrete"))
            doc.vSeg = _parse_valor(_text(icms, "vSeg"))
            doc.vDesc = _parse_valor(_text(icms, "vDesc"))
            doc.vII = _parse_valor(_text(icms, "vII"))
            doc.vIPI = _parse_valor(_text(icms, "vIPI"))
            doc.vIPIDevol = _parse_valor(_text(icms, "vIPIDevol"))
            doc.vPIS = _parse_valor(_text(icms, "vPIS"))
            doc.vCOFINS = _parse_valor(_text(icms, "vCOFINS"))
            doc.vOutro = _parse_valor(_text(icms, "vOutro"))
            doc.vTotTrib = _parse_valor(_text(icms, "vTotTrib"))

        ibs = _child(total, "IBSCBSTot")
        if ibs is not None:
            doc.vBCIBSCBS = _parse_valor(_text(ibs, "vBCIBSCBS"))
            gIBS = _child(ibs, "gIBS")
            if gIBS is not None:
                doc.vIBS = _parse_valor(_text(gIBS, "vIBS"))
                doc.vCredPresIBS = _parse_valor(_text(gIBS, "vCredPres"))
                gUF = _child(gIBS, "gIBSUF")
                if gUF is not None:
                    doc.vIBSUF = _parse_valor(_text(gUF, "vIBSUF"))
                gMun = _child(gIBS, "gIBSMun")
                if gMun is not None:
                    doc.vIBSMun = _parse_valor(_text(gMun, "vIBSMun"))
            gCBS = _child(ibs, "gCBS")
            if gCBS is not None:
                doc.vCBS = _parse_valor(_text(gCBS, "vCBS"))
                doc.vCredPresCBS = _parse_valor(_text(gCBS, "vCredPres"))
            gMono = _child(ibs, "gMono")
            if gMono is not None:
                doc.vIBSMono = _parse_valor(_text(gMono, "vIBSMono"))
                doc.vCBSMono = _parse_valor(_text(gMono, "vCBSMono"))
                doc.vIBSMonoReten = _parse_valor(_text(gMono, "vIBSMonoReten"))
                doc.vCBSMonoReten = _parse_valor(_text(gMono, "vCBSMonoReten"))
                doc.vIBSMonoRet = _parse_valor(_text(gMono, "vIBSMonoRet"))
                doc.vCBSMonoRet = _parse_valor(_text(gMono, "vCBSMonoRet"))
        doc.vNFTot = _parse_valor(_text(total, "vNFTot"))

    return doc


def _parse_status(root):
    evento_cancelado = False
    for el in root.iter():
        if _name(el.tag) == "infEvento":
            for d in el.iter():
                if _name(d.tag) == "cStat" and d.text and d.text.strip() == "135":
                    evento_cancelado = True
                    break

    prot = None
    for el in root.iter():
        if _name(el.tag) == "protNFe":
            prot = el
            break

    if prot is not None:
        inf = _child(prot, "infProt")
        if inf is not None:
            cstat = _text(inf, "cStat")
            if cstat == "135" or evento_cancelado:
                return STATUS_CANCELADA
            if cstat in CSTAT_DENEGADOS:
                return STATUS_DENEGADA
            if cstat == "100":
                return STATUS_AUTORIZADA
            return STATUS_REJEITADA
    if evento_cancelado:
        return STATUS_CANCELADA
    return STATUS_SEM_PROTOCOLO


def _parse_arbitrio(texto: str, arquivo):
    doc = Documento(arquivo)
    doc.erro = "Arquivo XML inválido"
    return [doc]


def _parse_evento(root, arquivo):
    chaves = []
    tem_135 = False

    for el in root.iter():
        if _name(el.tag) == "infEvento":
            det = _child(el, "detEvento")
            ddesc = _text(det, "descEvento") if det is not None else ""
            tpevento = _text(el, "tpEvento")
            chave = _text(el, "chNFe")
            if (tpevento == "110111" or "cancel" in ddesc.lower()) and chave:
                chaves.append(chave)
        elif _name(el.tag) == "infCanc":
            chave = _text(el, "chNFe")
            if chave:
                chaves.append(chave)

    for el in root.iter():
        if _name(el.tag) == "cStat" and el.text and el.text.strip() == "135":
            tem_135 = True

    if chaves and tem_135:
        doc = Documento(arquivo)
        doc.evento_cancelamento = True
        doc.evento = True
        doc.status = STATUS_CANCELAMENTO
        doc.chave = chaves[0]
        doc.modelo_nome = "Evento"
        doc.emitente = "Evento de cancelamento"
        return [doc]
    return None


def _parse_inutilizacao(root, arquivo):
    for el in root.iter():
        if _name(el.tag) == "infInut":
            cstat = _text(el, "cStat")
            if cstat in CSTAT_INUTILIZADA:
                doc = Documento(arquivo)
                doc.evento = True
                doc.status = STATUS_INUTILIZADA
                doc.modelo_nome = "Inutilização"
                doc.emitente = "Inutilização de numeração"
                try:
                    doc.modelo = int(_text(el, "mod") or "0")
                except ValueError:
                    doc.modelo = 0
                doc.serie = _text(el, "serie")
                ini = _text(el, "nNFIni")
                fim = _text(el, "nNFFin")
                if ini or fim:
                    doc.numero = (ini + "–" + fim) if ini and fim and ini != fim else (ini or fim)
                return [doc]
    return None


def _parse_cce(root, arquivo):
    for el in root.iter():
        if _name(el.tag) == "infEvento" and _text(el, "tpEvento") == "110110":
            doc = Documento(arquivo)
            doc.evento = True
            doc.status = STATUS_CCE
            doc.chave = _text(el, "chNFe")
            doc.modelo_nome = "Evento"
            doc.emitente = "Carta de correção"
            return [doc]
    return None


def _tem_procevento(root):
    for el in root.iter():
        if _name(el.tag) == "procEventoNFe":
            return True
    return False


def parse_arquivo_xml(dados: bytes, arquivo: str):
    try:
        root = ET.fromstring(dados)
    except (ET.ParseError, ValueError):
        return _parse_arbitrio(dados, arquivo)

    docs = []
    for el in root.iter():
        if _name(el.tag) == "NFe":
            inf = _child(el, "infNFe")
            if inf is None:
                continue
            doc = _parse_inf_nfe(inf, arquivo)
            doc.status = _parse_status(root)
            docs.append(doc)

    if not docs:
        evento = _parse_evento(root, arquivo)
        if evento is not None:
            return evento
        inut = _parse_inutilizacao(root, arquivo)
        if inut is not None:
            return inut
        cce = _parse_cce(root, arquivo)
        if cce is not None:
            return cce
        if _tem_procevento(root):
            doc = Documento(arquivo)
            doc.evento = True
            doc.status = STATUS_EVENTO
            doc.modelo_nome = "Evento"
            doc.emitente = "Evento"
            return [doc]
        doc = Documento(arquivo)
        doc.erro = "Não é um XML de NF-e/NFC-e"
        docs.append(doc)
    return docs


def ler_arquivo(arquivo: str):
    with open(arquivo, "rb") as f:
        return f.read()


def escanear_arquivo_xml(arquivo: str):
    if arquivo.lower().endswith(".zip"):
        return _escanear_zip(arquivo)
    dados = ler_arquivo(arquivo)
    return parse_arquivo_xml(dados, arquivo)


def _escanear_zip(arquivo: str):
    docs = []
    try:
        with zipfile.ZipFile(arquivo) as z:
            for nome in z.namelist():
                if nome.lower().endswith(".xml"):
                    docs.extend(parse_arquivo_xml(z.read(nome), f"{arquivo} :: {nome}"))
    except (zipfile.BadZipFile, OSError):
        doc = Documento(arquivo)
        doc.erro = "Arquivo ZIP inválido"
        docs.append(doc)
    return docs


def escanear_pasta(pasta: str, incluir_subpastas: bool = True, on_progress=None,
                   max_workers=None):
    arquivos = []
    for raiz, dirs, files in os.walk(pasta):
        if not incluir_subpastas:
            dirs[:] = []
        for nome in files:
            if nome.lower().endswith((".xml", ".zip")):
                arquivos.append(os.path.join(raiz, nome))

    total = len(arquivos)
    if total == 0:
        return []

    documentos = []
    contador = 0
    trava = threading.Lock()

    def _trabalhar(caminho):
        try:
            return escanear_arquivo_xml(caminho)
        except Exception as e:
            d = Documento(caminho)
            d.erro = f"Erro ao ler: {e}"
            return [d]

    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futuros = {pool.submit(_trabalhar, c): c for c in arquivos}
        for fut in as_completed(futuros):
            caminho = futuros[fut]
            try:
                documentos.extend(fut.result())
            except Exception as e:
                d = Documento(caminho)
                d.erro = f"Erro ao ler: {e}"
                documentos.append(d)
            with trava:
                contador += 1
                i = contador
            if on_progress:
                on_progress(i, total, os.path.basename(caminho))
    return documentos


def _rank_status(status):
    if status in (STATUS_CANCELADA, STATUS_DENEGADA):
        return 3
    if status == STATUS_AUTORIZADA:
        return 2
    if status.startswith("Rejeitada"):
        return 1
    return 0


def _status_final(doc, chaves_canceladas):
    if doc.chave and doc.chave in chaves_canceladas:
        return STATUS_CANCELADA
    return doc.status


def resumir(documentos, ignorar_duplicados=True, considerar_fcp=False):
    erros = []
    extras = []
    notas = []

    for doc in documentos:
        if doc.erro:
            erros.append(doc)
        elif doc.evento:
            extras.append(doc)
        else:
            notas.append(doc)

    chaves_canceladas = {e.chave for e in extras if e.evento_cancelamento}

    melhores = {}
    duplicados_removidos = 0

    for doc in notas:
        if ignorar_duplicados and doc.chave:
            if doc.chave in melhores:
                duplicados_removidos += 1
                atual = melhores[doc.chave]
                if (_rank_status(_status_final(doc, chaves_canceladas))
                        > _rank_status(_status_final(atual, chaves_canceladas))):
                    melhores[doc.chave] = doc
            else:
                melhores[doc.chave] = doc
        else:
            melhores.setdefault(id(doc), doc)

    total = Decimal("0")
    qtd = 0
    qtd_nfe = 0
    qtd_nfce = 0
    qtd_canceladas = 0
    resultados = []
    por_status = {}

    def acumular(status, q=1, valor=None):
        p = por_status.setdefault(status, {"qtd": 0, "total": Decimal("0")})
        p["qtd"] += q
        if valor is not None:
            p["total"] += valor

    for doc in melhores.values():
        status = _status_final(doc, chaves_canceladas)
        doc.status = status
        if status in (STATUS_CANCELADA, STATUS_DENEGADA):
            qtd_canceladas += 1
            acumular(status, 1, doc.valor if doc.valor is not None else Decimal("0"))
            resultados.append(doc)
            continue
        if doc.valor is not None:
            valor_efetivo = doc.valor
            if considerar_fcp:
                if doc.vFCP is not None:
                    valor_efetivo += doc.vFCP
                if doc.vFCPST is not None:
                    valor_efetivo += doc.vFCPST
                if doc.vFCPSTRet is not None:
                    valor_efetivo += doc.vFCPSTRet
            total += valor_efetivo
            qtd += 1
            if doc.modelo == 65:
                qtd_nfce += 1
            else:
                qtd_nfe += 1
        acumular(status, 1, doc.valor if doc.valor is not None else Decimal("0"))
        resultados.append(doc)

    for doc in extras:
        acumular(doc.status, 1)
    for doc in erros:
        acumular(STATUS_INVALIDA, 1)

    tributos = {chave: Decimal("0") for chave, _, _ in TRIBUTOS}
    for doc in resultados:
        for chave, _, _ in TRIBUTOS:
            v = getattr(doc, chave, None)
            if v is not None:
                tributos[chave] += v

    return {
        "total": total,
        "quantidade": qtd,
        "qtd_nfe": qtd_nfe,
        "qtd_nfce": qtd_nfce,
        "qtd_canceladas": qtd_canceladas,
        "qtd_ignoradas": len(erros),
        "qtd_extras": len(extras),
        "documentos": resultados,
        "extras": extras,
        "erros": erros,
        "duplicados_removidos": duplicados_removidos,
        "por_status": por_status,
        "tributos": tributos,
    }
