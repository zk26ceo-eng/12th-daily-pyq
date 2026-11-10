const cron = require('node-cron');
const fs = require('fs');
const path = require('path');

const prefsPath = process.env.USER_PREFS_PATH || path.join(__dirname, 'user-prefs.json');
const templatePath = path.join(__dirname, 'user-prefs-template.json');
const prefs = fs.existsSync(prefsPath)
  ? JSON.parse(fs.readFileSync(prefsPath, 'utf8'))
  : JSON.parse(fs.readFileSync(templatePath, 'utf8'));

async function sendMessage(recipient, message) {
  // Deliberate placeholder. Connect this to The Network or an approved provider.
  // Never put API keys in this file; use environment variables and consent checks.
  console.log(`[DRY RUN] ${recipient}:\n${message}`);
}

function validatePrefs(p) {
  if (!p || !Array.isArray(p.subjects) || p.subjects.length === 0) throw new Error('No subjects selected');
  if (!p.consentToMessages && process.env.ALLOW_DRY_RUN !== 'true') throw new Error('Messaging consent is required');
}

function dailyMessage(p) {
  const subjectNumbers = p.subjects.map((s, i) => `${i + 1}. ${s}: [load one PYQ from the selected board bank]`);
  return `Daily PYQ — ${p.language || 'English'}\n\n${subjectNumbers.join('\n')}\n\nReply with answers 1-${p.subjects.length}`;
}

validatePrefs(prefs);
const [hour, minute] = (prefs.dailyTime || '07:00').split(':');
cron.schedule(`${minute} ${hour} * * *`, async () => {
  await sendMessage(process.env.MESSAGE_RECIPIENT || 'study-group', dailyMessage(prefs));
}, { timezone: prefs.timezone || 'Asia/Kolkata' });
console.log(`12th Daily PYQ scheduler ready for ${prefs.dailyTime || '07:00'} ${prefs.timezone || 'Asia/Kolkata'}`);
