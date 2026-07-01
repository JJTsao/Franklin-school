const fs = require('node:fs');
const path = require('node:path');

const rootDir = path.resolve(__dirname, '..');
const distDir = path.resolve(rootDir, 'dist');

function copyTree(sourceDir, targetDir) {
  fs.mkdirSync(targetDir, { recursive: true });

  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    const sourcePath = path.join(sourceDir, entry.name);
    const targetPath = path.join(targetDir, entry.name);

    if (entry.isDirectory()) {
      copyTree(sourcePath, targetPath);
    } else if (entry.isFile()) {
      fs.copyFileSync(sourcePath, targetPath);
    }
  }
}

function verifySite(siteDir) {
  const htmlPath = path.join(siteDir, 'index.html');
  const cssPath = path.join(siteDir, 'src', 'styles.css');
  const html = fs.readFileSync(htmlPath, 'utf8');
  const css = fs.readFileSync(cssPath, 'utf8');
  const missing = [];

  for (const match of html.matchAll(/(?:src|href)="(\.\/[^"#]+)"/g)) {
    const targetPath = path.resolve(siteDir, match[1]);
    if (!fs.existsSync(targetPath)) missing.push(targetPath);
  }

  for (const match of css.matchAll(/url\(['"]?(\.\.\/[^'")]+)['"]?\)/g)) {
    const targetPath = path.resolve(path.dirname(cssPath), match[1]);
    if (!fs.existsSync(targetPath)) missing.push(targetPath);
  }

  const inlineScripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  for (const [, source] of inlineScripts) new Function(source);

  if (missing.length) {
    throw new Error(`Missing static assets:\n${missing.join('\n')}`);
  }
}

fs.mkdirSync(distDir, { recursive: true });
fs.copyFileSync(path.join(rootDir, 'index.html'), path.join(distDir, 'index.html'));
copyTree(path.join(rootDir, 'src'), path.join(distDir, 'src'));
copyTree(path.join(rootDir, 'public'), path.join(distDir, 'public'));

verifySite(rootDir);
verifySite(distDir);

console.log(`Static site built and verified at ${distDir}`);
