(() => {
  const branches = Object.freeze({
    douliu: Object.freeze({
      name: '斗六分校',
      address: '雲林縣斗六市中堅西路 306 號',
      phone: '05-535-3585',
      mapUrl: 'https://maps.app.goo.gl/j9AvbMegSyCXbRcX7',
      lineUrl: 'https://line.me/ti/p/vH8_IWausT',
      facebookUrl: 'https://www.facebook.com/sesamestreetTUZ/',
    }),
    dounan: Object.freeze({
      name: '斗南分校',
      address: '雲林縣斗南鎮中正路 362 號',
      phone: '05-595-3585',
      mapUrl: 'https://maps.app.goo.gl/LE9UxTEUGz2PJk4y7',
      lineUrl: 'https://line.me/ti/p/8ajiWmB8hV',
      facebookUrl: 'https://www.facebook.com/profile.php?id=100063597169844',
    }),
  });

  const descendantsAndSelf = (scope, selector) => [
    ...(scope.matches(selector) ? [scope] : []),
    ...scope.querySelectorAll(selector),
  ];

  document.querySelectorAll('[data-branch]').forEach((scope) => {
    const branch = branches[scope.dataset.branch];
    if (!branch) return;

    descendantsAndSelf(scope, '[data-branch-field]').forEach((element) => {
      const value = branch[element.dataset.branchField];
      if (value) element.textContent = value;
    });

    descendantsAndSelf(scope, '[data-branch-link]').forEach((link) => {
      const linkType = link.dataset.branchLink;
      const href = {
        map: branch.mapUrl,
        line: branch.lineUrl,
        facebook: branch.facebookUrl,
      }[linkType];

      if (href) link.href = href;
      if (linkType === 'map') link.setAttribute('aria-label', `在 Google 地圖開啟${branch.name}地址`);
      if (linkType === 'line') link.setAttribute('aria-label', `開啟${branch.name} LINE 加好友頁面（另開新視窗）`);
      if (linkType === 'facebook') link.setAttribute('aria-label', `開啟${branch.name} Facebook 粉絲專頁（另開新視窗）`);
    });
  });
})();
