// ============================================================
// Ruah Monitor — Google Apps Script Webhook
// Deploy como Web App:
//   Execute as: Me
//   Who has access: Anyone
// ============================================================

var SPREADSHEET_ID = '1TkN-PwEyTNByOC0Bz3nEM-qDf5cn68Y0NFWPBWiSx0g';

// Limites por plano
var LIMITES_PERFIS = {
  'basico':       1,
  'profissional': 3,
  'creditos':     1
};

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);

    var nome         = (data.nome         || '').trim();
    var email        = (data.email        || '').trim();
    var whatsapp     = (data.whatsapp     || '').replace(/\D/g, '');
    var keywords     = (data.keywords     || '').trim();
    var location     = (data.location     || '').trim();
    var tipoTrabalho = (data.tipo_trabalho|| 'todos').trim().toLowerCase();
    var plano        = (data.plano        || 'basico').trim().toLowerCase();

    // Validação mínima
    if (!nome || !whatsapp || !keywords) {
      return resposta(400, 'Campos obrigatórios ausentes.');
    }

    var ss      = SpreadsheetApp.openById(SPREADSHEET_ID);
    var wsClientes = ss.getSheetByName('clientes');
    var wsPerfis   = ss.getSheetByName('perfis_busca');

    // Gera client_id único
    var clientId = 'cli_' + new Date().getTime();
    var agora    = Utilities.formatDate(new Date(), 'America/Sao_Paulo', 'yyyy-MM-dd HH:mm:ss');

    // Verifica se WhatsApp já existe (evita duplicatas)
    var clientesData = wsClientes.getDataRange().getValues();
    for (var i = 1; i < clientesData.length; i++) {
      var wpExistente = String(clientesData[i][3]).replace(/\D/g, '');
      if (wpExistente === whatsapp) {
        return resposta(409, 'WhatsApp já cadastrado.');
      }
    }

    // Insere na aba clientes
    // Colunas: client_id | nome | email | whatsapp | status | plano | criado_em
    wsClientes.appendRow([clientId, nome, email, whatsapp, 'ativo', plano, agora]);

    // Insere na aba perfis_busca
    // Colunas: client_id | keywords | location | tipo_trabalho | intervalo_min | ativo
    var intervalo = 10; // minutos
    wsPerfis.appendRow([clientId, keywords, location, tipoTrabalho, intervalo, 'TRUE']);

    // Log de confirmação
    Logger.log('Novo cliente cadastrado: ' + clientId + ' — ' + nome + ' (' + plano + ')');

    return resposta(200, 'OK');

  } catch (err) {
    Logger.log('Erro no webhook: ' + err.message);
    return resposta(500, 'Erro interno: ' + err.message);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(
    JSON.stringify({ status: 'Ruah Monitor Webhook ativo' })
  ).setMimeType(ContentService.MimeType.JSON);
}

function resposta(codigo, msg) {
  return ContentService.createTextOutput(
    JSON.stringify({ codigo: codigo, mensagem: msg })
  ).setMimeType(ContentService.MimeType.JSON);
}
