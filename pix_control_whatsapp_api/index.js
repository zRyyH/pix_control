require('dotenv').config();

const wppconnect = require('@wppconnect-team/wppconnect');
const FormData = require('form-data');
const jwt = require('jsonwebtoken');
const axios = require('axios');


// Acessando o segredo do .env
const secret = process.env.SECRET_KEY;


// Geração do token
const token = jwt.sign({}, secret);


// Instanciação do axios com o token
const api = axios.create({
    baseURL: 'http://api:8000/api',
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
        console.log('Mensagem recebida:', message.from, message.to);

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
                        to_number: message.to.split("@")[0]
                    }
                });

                console.log('✅ Enviado para API:', response.data);
            } catch (err) {
                console.error('❌ Erro ao enviar para API:', err.message);
            }
        }
    });
}