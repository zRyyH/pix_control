require('dotenv').config();

const wppconnect = require('@wppconnect-team/wppconnect');
const FormData = require('form-data');
const jwt = require('jsonwebtoken');
const axios = require('axios');


// Acessando o segredo do .env
const secret = process.env.SECRET_KEY;


// Obtendo IP da API
const ip = process.env.API_IP || 'localhost:8000';


// Geração do token
const token = jwt.sign({}, secret);


// Instanciação do axios com o token
const api = axios.create({
    baseURL: `http://${ip}/api`,
    timeout: 60000,
    headers: {
        Authorization: `Bearer ${token}`
    }
});


// Configuração do cliente WPPConnect
wppconnect
    .create({
        session: 'zap-bot',
        headless: true,
        logQR: true,
        autoClose: false,
        qrTimeout: 0,
        puppeteerOptions: {
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        }
    })
    .then(client => start(client))
    .catch(err => console.error(err));


// Função para iniciar o cliente e escutar mensagens
function start(client) {
    client.onAnyMessage(async (message) => {
        console.log('Mensagem recebida:', 'de:', message.from, 'para:', message.to, 'autor:', message.author);

        if (message.mimetype) {
            const media = await client.decryptFile(message);
            const ext = message.mimetype.split('/')[1];
            const filename = `${Date.now()}.${ext}`;

            const form = new FormData();

            form.append('file', Buffer.from(media), {
                filename,
                contentType: message.mimetype
            });

            try {
                const response = await api.post('/validar-comprovante', form, {
                    headers: {
                        ...form.getHeaders()
                    },
                    params: {
                        from_number: message.from.split("@")[0],
                        to_number: message.to.split("@")[0],
                        author_number: message.author ? message.author.split("@")[0] : 0,
                        is_group_msg: message.isGroupMsg ? 1 : 0,
                        from_me: message.fromMe ? 1 : 0,
                        timestamp: message.t,
                    }
                });

                console.log('✅ Enviado para API:', response.data);
            } catch (err) {
                console.error('❌ Erro ao enviar para API:', err.message);
            }
        }
    });
}