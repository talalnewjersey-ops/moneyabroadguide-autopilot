<?php
/**
 * Plugin Name: MAG Autopilot Connector
 * Description: Connects WordPress with GitHub Autopilot system + Ebook Conversion Suite
 * Version: 2.0
 */

if (!defined('ABSPATH')) exit;

// 🔐 API KEY
define('MAG_API_KEY', 'MAG_2026_Talal_Secure_80..@@$$RaAmMeTA');

// ─── CONSTANTS ───────────────────────────────────────────────────────────────
define('MAG_EBOOK_URL',     'https://moneyabroadguide.com/build-your-credit-score-in-the-usa-2026-edition/');
define('MAG_CHECKOUT_URL',  'https://moneyabroadguide.gumroad.com/l/vemvxw');
define('MAG_EBOOK_TITLE',   'Build Your Credit Score in the USA – 2026 Edition');
define('MAG_EBOOK_PRICE',   '$19.99');
define('MAG_EBOOK_SLUG',    'build-your-credit-score-in-the-usa-2026-edition');
define('MAG_BRAND_GREEN',   '#1a9e5f');
define('MAG_BRAND_GREEN_D', '#157a49'); // darker hover

// ─── STATUS ENDPOINT ─────────────────────────────────────────────────────────
add_action('rest_api_init', function () {
    register_rest_route('mag/v1', '/status', [
        'methods'  => 'GET',
        'callback' => function () {
            return [
                'status' => 'connected',
                'site'   => get_bloginfo('name'),
                'url'    => home_url(),
            ];
        },
        'permission_callback' => '__return_true',
    ]);
});

// ─── SHARED STYLES ───────────────────────────────────────────────────────────
add_action('wp_head', 'mag_global_styles');
function mag_global_styles() {
    ?>
    <style id="mag-ebook-styles">
    /* ── Ebook CTA button in desktop nav ── */
    .mag-ebook-nav-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: <?php echo MAG_BRAND_GREEN; ?>;
        color: #fff !important;
        font-weight: 700;
        font-size: 14px;
        padding: 9px 18px;
        border-radius: 6px;
        text-decoration: none !important;
        white-space: nowrap;
        transition: background .2s ease, transform .15s ease, box-shadow .2s ease;
        box-shadow: 0 2px 8px rgba(26,158,95,.35);
        order: -1;
    }
    .mag-ebook-nav-btn:hover {
        background: <?php echo MAG_BRAND_GREEN_D; ?>;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(26,158,95,.45);
        color: #fff !important;
    }
    .mag-ebook-nav-btn svg { flex-shrink: 0; }

    /* ── Mobile nav ebook item ── */
    .mag-ebook-mobile-item {
        display: block;
        background: <?php echo MAG_BRAND_GREEN; ?>;
        color: #fff !important;
        font-weight: 700;
        font-size: 16px;
        padding: 14px 20px;
        text-align: center;
        border-radius: 8px;
        margin: 8px 12px 4px;
        text-decoration: none !important;
        box-shadow: 0 2px 8px rgba(26,158,95,.35);
    }
    .mag-ebook-mobile-item:hover { background: <?php echo MAG_BRAND_GREEN_D; ?>; color: #fff !important; }

    /* ── Homepage promotional banner ── */
    #mag-promo-banner {
        background: linear-gradient(135deg, #0d3b26 0%, #1a9e5f 100%);
        color: #fff;
        padding: 22px 20px;
        text-align: center;
        position: relative;
        z-index: 100;
    }
    #mag-promo-banner .mag-pb-eyebrow {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #a8f5d2;
        margin-bottom: 6px;
    }
    #mag-promo-banner .mag-pb-title {
        font-size: clamp(18px, 4vw, 26px);
        font-weight: 800;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    #mag-promo-banner .mag-pb-price {
        font-size: 15px;
        margin-bottom: 16px;
        color: #cffce5;
    }
    #mag-promo-banner .mag-pb-price strong {
        color: #fff;
        font-size: 22px;
    }
    #mag-promo-banner .mag-pb-btn {
        display: inline-block;
        background: #fff;
        color: #0d3b26 !important;
        font-weight: 800;
        font-size: 15px;
        padding: 12px 32px;
        border-radius: 50px;
        text-decoration: none !important;
        transition: transform .15s ease, box-shadow .2s ease;
        box-shadow: 0 4px 14px rgba(0,0,0,.25);
    }
    #mag-promo-banner .mag-pb-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,.35);
    }
    #mag-promo-banner .mag-pb-close {
        position: absolute;
        top: 10px;
        right: 14px;
        background: none;
        border: none;
        color: rgba(255,255,255,.7);
        font-size: 20px;
        cursor: pointer;
        line-height: 1;
        padding: 4px;
    }
    #mag-promo-banner .mag-pb-close:hover { color: #fff; }

    /* ── Sticky bottom mobile CTA ── */
    #mag-sticky-cta {
        display: none;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #fff;
        border-top: 2px solid #e5e7eb;
        z-index: 9999;
        padding: 10px 16px;
        padding-bottom: calc(10px + env(safe-area-inset-bottom, 0px));
        box-shadow: 0 -4px 16px rgba(0,0,0,.12);
        align-items: center;
        gap: 12px;
    }
    @media (max-width: 768px) {
        #mag-sticky-cta { display: flex; }
    }
    #mag-sticky-cta .mag-sc-text { flex: 1; min-width: 0; }
    #mag-sticky-cta .mag-sc-name {
        font-weight: 700;
        font-size: 13px;
        color: #111;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    #mag-sticky-cta .mag-sc-price {
        font-size: 12px;
        color: #555;
    }
    #mag-sticky-cta .mag-sc-btn {
        display: inline-block;
        background: <?php echo MAG_BRAND_GREEN; ?>;
        color: #fff !important;
        font-weight: 700;
        font-size: 13px;
        padding: 11px 20px;
        border-radius: 6px;
        text-decoration: none !important;
        white-space: nowrap;
        flex-shrink: 0;
    }
    #mag-sticky-cta .mag-sc-close {
        background: none;
        border: none;
        color: #999;
        font-size: 18px;
        cursor: pointer;
        flex-shrink: 0;
        padding: 0 4px;
    }
    </style>
    <?php
}

// ─── DESKTOP NAV EBOOK CTA ────────────────────────────────────────────────────
// Injects the ebook button into the primary navigation via JS (theme-agnostic)
add_action('wp_footer', 'mag_nav_ebook_cta', 5);
function mag_nav_ebook_cta() {
    $book_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>';
    ?>
    <script>
    (function(){
        var EBOOK_URL = <?php echo json_encode(MAG_EBOOK_URL); ?>;
        var BOOK_SVG  = <?php echo json_encode($book_svg); ?>;

        function buildBtn(extraClass) {
            var a = document.createElement('a');
            a.href = EBOOK_URL;
            a.className = 'mag-ebook-nav-btn' + (extraClass ? ' ' + extraClass : '');
            a.setAttribute('data-mag-ebook', '1');
            a.setAttribute('aria-label', 'Get the Ebook – Build Your Credit Score in the USA');
            a.innerHTML = BOOK_SVG + '<span class="mag-ebook-btn-text">GET YOUR EBOOK NOW</span>';
            function updateText() {
                var span = a.querySelector('.mag-ebook-btn-text');
                if (span) span.textContent = window.innerWidth < 500 ? 'GET THE EBOOK' : 'GET YOUR EBOOK NOW';
            }
            updateText();
            window.addEventListener('resize', updateText);
            return a;
        }

        // PRIMARY STRATEGY: anchor to the real "Compare Fees Now" control and
        // insert our ebook CTA immediately BEFORE it — wherever it renders
        // (desktop header AND mobile menu). This is theme-agnostic because it
        // keys off the button the user can already see, not guessed selectors.
        function injectBeforeCompare() {
            var done = false;
            var controls = document.querySelectorAll('a, button');
            for (var i = 0; i < controls.length; i++) {
                var el = controls[i];
                var txt = (el.textContent || '').trim().toLowerCase();
                if (txt.indexOf('compare fees') === -1) continue;
                // Skip if our button is already the immediately-preceding sibling.
                var prev = el.previousElementSibling;
                if (prev && prev.getAttribute && prev.getAttribute('data-mag-ebook')) { done = true; continue; }
                var target = el;
                // If the compare control is wrapped in an <li>, insert a sibling <li>.
                if (el.parentNode && el.parentNode.tagName === 'A') target = el.parentNode;
                if (el.closest) { var li = el.closest('li'); if (li && li.parentNode) {
                    var wrap = document.createElement('li');
                    wrap.className = 'mag-ebook-nav-item';
                    wrap.appendChild(buildBtn());
                    li.parentNode.insertBefore(wrap, li);
                    done = true; continue;
                }}
                target.parentNode.insertBefore(buildBtn(), target);
                done = true;
            }
            return done;
        }

        // FALLBACK: drop into the first nav <ul> we can find.
        function injectIntoNav() {
            if (document.querySelector('[data-mag-ebook]')) return true;
            var selectors = ['.main-navigation ul','#primary-menu','header nav ul',
                             '.nav-menu','.navbar-nav','.nav-links','nav ul'];
            for (var i = 0; i < selectors.length; i++) {
                var nav = document.querySelector(selectors[i]);
                if (nav) {
                    var li = document.createElement('li');
                    li.className = 'mag-ebook-nav-item';
                    li.appendChild(buildBtn());
                    nav.insertBefore(li, nav.firstChild);
                    return true;
                }
            }
            return false;
        }

        function run() {
            if (!injectBeforeCompare()) injectIntoNav();
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', run);
        } else { run(); }

        // Re-run on dynamic menu changes (hamburger toggles, JS-hydrated themes,
        // off-canvas menus that render their links only when opened). Debounced.
        var t;
        var mo = new MutationObserver(function(){
            clearTimeout(t);
            t = setTimeout(run, 150);
        });
        mo.observe(document.body, { childList: true, subtree: true });
        // Stop observing after 20s to avoid perpetual work.
        setTimeout(function(){ mo.disconnect(); }, 20000);
    })();
    </script>
    <?php
}

// ─── HOMEPAGE PROMOTIONAL BANNER ─────────────────────────────────────────────
add_action('wp_footer', 'mag_homepage_promo_banner', 10);
function mag_homepage_promo_banner() {
    if (!is_front_page() && !is_home()) return;
    ?>
    <div id="mag-promo-banner" role="region" aria-label="Ebook promotion">
        <button class="mag-pb-close" id="mag-pb-close-btn" aria-label="Close promotion">&times;</button>
        <div class="mag-pb-eyebrow">New for 2026</div>
        <div class="mag-pb-title">Build Your Credit Score in the USA</div>
        <div class="mag-pb-price">Special Launch Price: <strong><?php echo MAG_EBOOK_PRICE; ?></strong></div>
        <a href="<?php echo esc_url(MAG_CHECKOUT_URL); ?>" class="mag-pb-btn">Get Instant Access</a>
    </div>
    <script>
    (function(){
        var banner = document.getElementById('mag-promo-banner');
        var closeBtn = document.getElementById('mag-pb-close-btn');

        if (!banner) return;

        // Respect user dismissal (sessionStorage so it reappears next visit)
        if (sessionStorage.getItem('mag_banner_dismissed')) {
            banner.style.display = 'none';
            return;
        }

        // Move banner to just after <header> for maximum visibility
        var header = document.querySelector('header.site-header, header#masthead, header[role="banner"], header');
        if (header && header.parentNode) {
            header.parentNode.insertBefore(banner, header.nextSibling);
        } else {
            document.body.insertBefore(banner, document.body.firstChild);
        }

        closeBtn && closeBtn.addEventListener('click', function() {
            banner.style.display = 'none';
            sessionStorage.setItem('mag_banner_dismissed', '1');
        });
    })();
    </script>
    <?php
}

// ─── STICKY MOBILE CTA (ebook landing page + all pages) ──────────────────────
add_action('wp_footer', 'mag_sticky_mobile_cta', 20);
function mag_sticky_mobile_cta() {
    ?>
    <div id="mag-sticky-cta" role="complementary" aria-label="Ebook offer">
        <div class="mag-sc-text">
            <div class="mag-sc-name">Build Your Credit Score in the USA</div>
            <div class="mag-sc-price"><?php echo MAG_EBOOK_PRICE; ?></div>
        </div>
        <a href="<?php echo esc_url(MAG_CHECKOUT_URL); ?>" class="mag-sc-btn">GET INSTANT ACCESS</a>
        <button class="mag-sc-close" id="mag-sc-close-btn" aria-label="Close">&times;</button>
    </div>
    <script>
    (function(){
        var cta   = document.getElementById('mag-sticky-cta');
        var close = document.getElementById('mag-sc-close-btn');
        if (!cta || !close) return;
        if (localStorage.getItem('mag_sticky_dismissed')) { cta.style.display = 'none'; return; }
        close.addEventListener('click', function() {
            cta.style.display = 'none';
            localStorage.setItem('mag_sticky_dismissed', '1');
        });
    })();
    </script>
    <?php
}
