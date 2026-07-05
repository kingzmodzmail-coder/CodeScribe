import * as vscode from 'vscode';

const API_URL = 'http://localhost:8000/chat';

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('codescribe.openChat', () => {
    const panel = vscode.window.createWebviewPanel(
      'codescribe',
      'CodeScribe',
      vscode.ViewColumn.Beside,
      { enableScripts: true, retainContextWhenHidden: true }
    );

    panel.webview.html = getWebviewContent();

    panel.webview.onDidReceiveMessage(async (message) => {
      if (message.command === 'ask') {
        try {
          const res = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: message.messages, mode: 'agent' }),
          });
          const data = await res.json();
          panel.webview.postMessage({ command: 'reply', text: data.reply });
        } catch (e: any) {
          panel.webview.postMessage({ command: 'reply', text: `Error: ${e.message}` });
        }
      }
    });
  });

  context.subscriptions.push(disposable);
}

function getWebviewContent(): string {
  return `<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: sans-serif; padding: 1rem; color: var(--vscode-foreground); }
    #history { border: 1px solid var(--vscode-panel-border); height: 60vh; overflow-y: auto; padding: 1rem; margin-bottom: 1rem; }
    #input-row { display: flex; gap: 0.5rem; }
    input { flex: 1; padding: 0.5rem; background: var(--vscode-input-background); color: var(--vscode-input-foreground); border: 1px solid var(--vscode-input-border); }
    button { padding: 0.5rem 1rem; }
  </style>
</head>
<body>
  <h2>CodeScribe</h2>
  <div id="history"></div>
  <div id="input-row">
    <input id="msg" placeholder="Ask about the current project..." />
    <button id="send">Send</button>
  </div>
  <script>
    const vscode = acquireVsCodeApi();
    let messages = [];

    document.getElementById('send').addEventListener('click', send);
    document.getElementById('msg').addEventListener('keypress', e => { if (e.key === 'Enter') send(); });

    window.addEventListener('message', event => {
      const m = event.data;
      if (m.command === 'reply') {
        messages.push({ role: 'assistant', content: m.text });
        render();
      }
    });

    function send() {
      const input = document.getElementById('msg');
      messages.push({ role: 'user', content: input.value });
      vscode.postMessage({ command: 'ask', messages });
      render();
      input.value = '';
    }

    function render() {
      document.getElementById('history').innerHTML = messages
        .map(m => '<div><b>' + m.role + ':</b> ' + escapeHtml(m.content) + '</div>')
        .join('');
    }

    function escapeHtml(text) {
      return text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
    }
  </script>
</body>
</html>`;
}
