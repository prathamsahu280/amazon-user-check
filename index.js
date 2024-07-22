const express = require('express');
const fetch = require('node-fetch');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

async function checkUserExistence(phoneNumber) {
  try {
    const response = await fetch("https://www.amazon.in/ap/signin", {
      "headers": {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
        "sec-ch-ua-mobile": "?0",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
      },
      "referrer": "https://www.amazon.in/ap/signin",
      "referrerPolicy": "strict-origin-when-cross-origin",
      "body": `appActionToken=&appAction=SIGNIN_PWD_COLLECT&subPageType=SignInClaimCollect&openid.return_to=&prevRID=&workflowState=&email=${encodeURIComponent(phoneNumber)}&password=&create=0&metadata1=`,
      "method": "POST",
      "mode": "cors"
    });

    const text = await response.text();
    return text.includes('auth-password-missing-alert');
  } catch (error) {
    console.error(`Error in checkUserExistence: ${error}`);
    return false;
  }
}

app.post('/api/check_user', async (req, res) => {
  const phoneNumber = req.body.phone_number;
  if (!phoneNumber) {
    return res.status(400).json({ error: "Phone number is required" });
  }

  try {
    const result = await checkUserExistence(phoneNumber);
    res.json({ exists: result });
  } catch (error) {
    console.error(`Error in /api/check_user: ${error}`);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.get('/', (req, res) => {
  res.send("Welcome to the Amazon User Checker API");
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
}).on('error', (err) => {
  console.error('Error starting server:', err);
});

process.on('uncaughtException', (err) => {
  console.error('Uncaught Exception:', err);
});

process.on('unhandledRejection', (reason, promise) => {
  console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

module.exports = app;