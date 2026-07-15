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

function extractHtmlReferences(html) {
  const references = [];

  for (const match of html.matchAll(/\b(src|href|srcset)\s*=\s*(["'])(.*?)\2/g)) {
    const [, attribute, , value] = match;

    if (attribute === 'srcset') {
      for (const candidate of value.split(',')) {
        const [reference] = candidate.trim().split(/\s+/);
        if (reference) references.push(reference);
      }
    } else {
      references.push(value);
    }
  }

  return references;
}

function extractCssReferences(css) {
  return [...css.matchAll(/url\(\s*(["']?)(.*?)\1\s*\)/g)].map((match) => match[2]);
}

function verifyReferences(references, sourcePath, siteDir, problems) {
  const sourceLabel = path.relative(siteDir, sourcePath);

  for (const reference of references) {
    if (!reference || reference.startsWith('#') || /^(?:[a-z][a-z0-9+.-]*:|\/\/)/i.test(reference)) continue;

    const cleanReference = reference.split(/[?#]/)[0];
    if (!cleanReference) continue;

    if (cleanReference.startsWith('/')) {
      problems.push(`${sourceLabel}: root-relative reference is not offline-safe: ${reference}`);
      continue;
    }

    let decodedReference;
    try {
      decodedReference = decodeURIComponent(cleanReference);
    } catch {
      problems.push(`${sourceLabel}: invalid URL encoding: ${reference}`);
      continue;
    }

    const targetPath = path.resolve(path.dirname(sourcePath), decodedReference);
    const relativeTarget = path.relative(siteDir, targetPath);
    const escapesSite = relativeTarget === '..' || relativeTarget.startsWith(`..${path.sep}`) || path.isAbsolute(relativeTarget);

    if (escapesSite) {
      problems.push(`${sourceLabel}: reference escapes the site directory: ${reference}`);
    } else if (!fs.existsSync(targetPath)) {
      problems.push(`${sourceLabel}: missing local asset: ${reference}`);
    }
  }
}

function verifySite(siteDir) {
  const htmlPath = path.join(siteDir, 'index.html');
  const cssPath = path.join(siteDir, 'src', 'styles.css');
  const html = fs.readFileSync(htmlPath, 'utf8');
  const css = fs.readFileSync(cssPath, 'utf8');
  const problems = [];

  verifyReferences(extractHtmlReferences(html), htmlPath, siteDir, problems);
  verifyReferences(extractCssReferences(css), cssPath, siteDir, problems);

  const inlineScripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  for (const [, source] of inlineScripts) new Function(source);

  if (problems.length) {
    throw new Error(`Static site verification failed:\n${[...new Set(problems)].join('\n')}`);
  }
}

fs.mkdirSync(distDir, { recursive: true });
fs.copyFileSync(path.join(rootDir, 'index.html'), path.join(distDir, 'index.html'));
// 自包含的預覽頁（若存在）：讓合作夥伴在同一網址預覽新版，首頁維持現況。
const previewSrc = path.join(rootDir, 'index-preview.html');
if (fs.existsSync(previewSrc)) {
  fs.copyFileSync(previewSrc, path.join(distDir, 'index-preview.html'));
}
copyTree(path.join(rootDir, 'src'), path.join(distDir, 'src'));
copyTree(path.join(rootDir, 'public'), path.join(distDir, 'public'));

verifySite(rootDir);
verifySite(distDir);

console.log(`Static site built and verified at ${distDir}`);
