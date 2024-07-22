const express = require('express');
const puppeteer = require('puppeteer');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

async function checkUserExistence(phoneNumber) {
  let browser;
  try {
    // Check if we're running on Vercel
    if (process.env.VERCEL) {
      // Use chrome-aws-lambda
      const chromium = require('chrome-aws-lambda');
      browser = await puppeteer.launch({
        args: chromium.args,
        defaultViewport: chromium.defaultViewport,
        executablePath: await chromium.executablePath,
        headless: chromium.headless,
      });
    } else {
      // Running locally, use regular Puppeteer
      browser = await puppeteer.launch();
    }

    const page = await browser.newPage();
    await page.goto("https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0");

    await page.type("#ap_email", phoneNumber);
    await page.click("#continue");

    await page.waitForSelector("#auth-password-missing-alert", { timeout: 5000 });
    return true;
  } catch (error) {
    console.error(`Error in checkUserExistence: ${error}`);
    return false;
  } finally {
    if (browser) {
      await browser.close();
    }
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