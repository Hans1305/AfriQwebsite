// AfriQ Header + Eyebrow self-heal for cached page restores and legacy templates
(function () {
  function isFirstPage() {
    var p = (location.pathname || "/").replace(/\/+$/, "");
    if (p === "/" || p === "") return true;
    var tail = p.split("/").pop();
    return tail === "index_new.html";
  }
  function pathPrefix() {
    var p = (location.pathname || "/").replace(/\/+$/, "");
    var parts = p.split("/").filter(Boolean);
    var isFile = parts.length && /\.[a-z0-9]+$/i.test(parts[parts.length - 1]);
    var depth = parts.length - (isFile ? 1 : 0);
    return depth > 0 ? Array(depth).fill("..").join("/") + "/" : "";
  }

  function ensureAfriqHeader(prefix) {
    if (document.querySelector(".afriq-header")) return;
    var wrapper = document.createElement("div");
    wrapper.innerHTML =
      '<header class="afriq-header">' +
      '  <div class="afriq-container">' +
      '    <div class="afriq-header__row">' +
      '      <a class="afriq-header__logo" href="' + prefix + 'index_new.html">' +
      '        <div>' +
      '          <img src="' + prefix + 'wp-content/uploads/2020/08/Q%20-%202.png" alt="AfriQ ArtisanSkills" style="width:min(29px, 8.5vw); height:auto; display:block;" />' +
      '          <div style="font-weight:900; letter-spacing:-.01em; color:#fff; margin-top:10px;">AfriQ ArtisanSkills</div>' +
      '        </div>' +
      '      </a>' +
      '      <nav class="afriq-nav" aria-label="Primary">' +
      '        <a href="' + prefix + 'solutions/">Solutions</a>' +
      '        <a href="' + prefix + 'industries/">Industries</a>' +
      '        <a href="' + prefix + 'training/courses/catalog/">Course Catalogue</a>' +
      '        <a href="' + prefix + 'resources.html">Resources</a>' +
      '        <a href="' + prefix + 'about/">About</a>' +
      '        <a href="' + prefix + 'contact/">Contact</a>' +
      '      </nav>' +
      '    </div>' +
      '  </div>' +
      '</header>';
    document.body.insertBefore(wrapper.firstElementChild, document.body.firstChild);
  }

  function ensureEyebrowHeader(prefix) {
    var eyebrow = document.querySelector(".hero .eyebrow");
    if (!eyebrow) return;
    var hasImg = !!eyebrow.querySelector("img");
    var hasText = eyebrow.textContent && eyebrow.textContent.indexOf("AfriQ ArtisanSkills") !== -1;
    if (hasImg && hasText) return;
    eyebrow.setAttribute("style", "display:flex; align-items:flex-start;");
    eyebrow.innerHTML =
      '<div style="display:flex; flex-direction:column; align-items:flex-start; gap:8px;">' +
      '  <img src="' + prefix + 'wp-content/uploads/2020/08/Q%20-%202.png" alt="AfriQ ArtisanSkills" style="width:min(58px, 17vw); height:auto; display:block;">' +
      '  <div style="font-weight:900; letter-spacing:-.01em; color:#fff; margin-top:10px;">AfriQ ArtisanSkills</div>' +
      '</div>';
  }

  function applyFixes() {
    if (isFirstPage()) return;
    var prefix = pathPrefix();
    ensureAfriqHeader(prefix);
    ensureEyebrowHeader(prefix);
  }

  window.addEventListener("DOMContentLoaded", applyFixes);
  window.addEventListener("pageshow", applyFixes);
})();
