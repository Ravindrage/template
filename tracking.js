/*!
 * Guruom Computers – visitor source tracking
 * Add to every page just before </body>:  <script src="tracking.js" defer></script>
 *
 * What it does
 *  1. Reads utm_source / utm_medium / utm_campaign / utm_content / utm_term, gclid, fbclid
 *  2. Falls back to the referrer (google, linkedin, freelancer...) or "direct"
 *  3. Saves FIRST visit and LATEST visit for 90 days (first-party cookie)
 *  4. Fills hidden fields in any <form> so every enquiry arrives with its source
 *  5. Adds the source to WhatsApp message text
 *  6. Sends the source to Google Analytics 4 if it is installed
 *
 * Email links must carry UTM tags, because email apps rarely send a referrer, e.g.
 *   https://ravindragehlot.com/portfolio.html?utm_source=email&utm_medium=email&utm_campaign=agency-outreach
 */
(function () {
  var COOKIE = 'gc_src', DAYS = 90;

  function getCookie(n) {
    var m = document.cookie.match('(?:^|; )' + n + '=([^;]*)');
    if (!m) return null;
    try { return JSON.parse(decodeURIComponent(m[1])); } catch (e) { return null; }
  }
  function setCookie(n, v) {
    var d = new Date(); d.setTime(d.getTime() + DAYS * 864e5);
    document.cookie = n + '=' + encodeURIComponent(JSON.stringify(v)) +
      ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
  }

  function classifyReferrer() {
    var ref = document.referrer;
    if (!ref) return { source: 'direct', medium: 'none' };
    var host;
    try { host = new URL(ref).hostname.replace(/^www\./, ''); } catch (e) { return { source: 'direct', medium: 'none' }; }
    if (host === location.hostname.replace(/^www\./, '')) return null; // internal navigation
    var search = /(^|\.)(google|bing|duckduckgo|yahoo|baidu|yandex)\./;
    var social = /(linkedin|facebook|instagram|twitter|t\.co|x\.com|youtube|reddit|whatsapp)/;
    if (search.test(host)) return { source: host.split('.')[host.split('.').length > 2 ? 1 : 0], medium: 'organic' };
    if (/freelancer\./.test(host)) return { source: 'freelancer', medium: 'referral' };
    if (/mail\.|outlook|gmail|yahoo\.com\/mail/.test(host)) return { source: 'email', medium: 'email' };
    if (social.test(host)) return { source: host.replace(/\.(com|in)$/, ''), medium: 'social' };
    return { source: host, medium: 'referral' };
  }

  function readCurrent() {
    var p = new URLSearchParams(location.search);
    var utm = p.get('utm_source');
    var data = {
      source: utm, medium: p.get('utm_medium'), campaign: p.get('utm_campaign'),
      content: p.get('utm_content'), term: p.get('utm_term'),
      gclid: p.get('gclid'), fbclid: p.get('fbclid')
    };
    if (!utm) {
      if (data.gclid) { data.source = 'google'; data.medium = 'cpc'; }
      else if (data.fbclid) { data.source = 'facebook'; data.medium = 'paid-social'; }
      else {
        var r = classifyReferrer();
        if (!r) return null;
        data.source = r.source; data.medium = r.medium;
      }
    }
    data.landing = location.pathname;
    data.time = new Date().toISOString();
    return data;
  }

  var store = getCookie(COOKIE) || {};
  var cur = readCurrent();
  // Keep the first visit forever (90 days); only overwrite "last" when the source is not just "direct"
  if (cur) {
    if (!store.first) store.first = cur;
    if (cur.source !== 'direct' || !store.last) store.last = cur;
    setCookie(COOKIE, store);
  }
  var first = store.first || {}, last = store.last || {};
  var label = (last.source || 'direct') + ' / ' + (last.medium || 'none') +
              (last.campaign ? ' / ' + last.campaign : '');

  function fillForms() {
    var fields = {
      source: last.source, medium: last.medium, campaign: last.campaign,
      first_source: first.source, first_medium: first.medium, landing_page: first.landing
    };
    document.querySelectorAll('form').forEach(function (f) {
      Object.keys(fields).forEach(function (k) {
        var name = 'utm_' + k;
        var el = f.querySelector('input[name="' + name + '"]');
        if (!el) {
          el = document.createElement('input');
          el.type = 'hidden'; el.name = name; f.appendChild(el);
        }
        el.value = fields[k] || '';
      });
    });
  }

  function tagWhatsApp() {
    document.querySelectorAll('a[href*="wa.me"]').forEach(function (a) {
      try {
        var u = new URL(a.href);
        var t = u.searchParams.get('text') || '';
        if (t.indexOf('[src:') === -1) {
          u.searchParams.set('text', t + ' [src: ' + label + ']');
          a.href = u.toString();
        }
      } catch (e) {}
    });
  }

  function sendAnalytics() {
    if (typeof window.gtag === 'function') {
      window.gtag('event', 'visitor_source', {
        first_source: first.source, first_medium: first.medium,
        last_source: last.source, last_medium: last.medium, last_campaign: last.campaign
      });
      document.addEventListener('click', function (e) {
        var a = e.target.closest && e.target.closest('a[href*="wa.me"],a[href*="contact.html"]');
        if (a) window.gtag('event', 'generate_lead_click', { method: a.href.indexOf('wa.me') > -1 ? 'whatsapp' : 'contact_page', source: label });
      });
    }
  }

  function init() { fillForms(); tagWhatsApp(); sendAnalytics(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();

  // Handy for debugging: type  guruomSource  in the browser console
  window.guruomSource = { first: first, last: last, label: label };
})();
