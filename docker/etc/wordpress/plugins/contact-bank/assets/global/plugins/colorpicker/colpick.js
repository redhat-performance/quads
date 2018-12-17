! function(t) {
var a = function() {
var a = '<div class="colpick"><div class="colpick_color"><div class="colpick_color_overlay1"><div class="colpick_color_overlay2"><div class="colpick_selector_outer"><div class="colpick_selector_inner"></div></div></div></div></div><div class="colpick_hue"><div class="colpick_hue_arrs"><div class="colpick_hue_larr"></div><div class="colpick_hue_rarr"></div></div></div><div class="colpick_new_color"></div><div class="colpick_current_color"></div><div class="colpick_hex_field"><div class="colpick_field_letter">#</div><input type="text" maxlength="6" size="6" /></div><div class="colpick_rgb_r colpick_field"><div class="colpick_field_letter">R</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_rgb_g colpick_field"><div class="colpick_field_letter">G</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_rgb_b colpick_field"><div class="colpick_field_letter">B</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_hsb_h colpick_field"><div class="colpick_field_letter">H</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_hsb_s colpick_field"><div class="colpick_field_letter">S</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_hsb_b colpick_field"><div class="colpick_field_letter">B</div><input type="text" maxlength="3" size="3" /><div class="colpick_field_arrs"><div class="colpick_field_uarr"></div><div class="colpick_field_darr"></div></div></div><div class="colpick_submit"></div></div>',
        e = {
        showEvent: "click",
                onShow: function() {},
                onBeforeShow: function() {},
                onHide: function() {},
                onChange: function() {},
                onSubmit: function() {},
                colorScheme: "light",
                color: "3289c7",
                livePreview: !0,
                flat: !1,
                layout: "full",
                submit: 1,
                submitText: "OK",
                height: 156
        },
        l = function(a, e) {
        var i = c(a);
                t(e).data("colpick").fields.eq(1).val(i.r).end().eq(2).val(i.g).end().eq(3).val(i.b).end()
        },
        r = function(a, e) {
        t(e).data("colpick").fields.eq(4).val(Math.round(a.h)).end().eq(5).val(Math.round(a.s)).end().eq(6).val(Math.round(a.b)).end()
        },
        n = function(a, e) {
        t(e).data("colpick").fields.eq(0).val(d(a))
        },
        s = function(a, e) {
        t(e).data("colpick").selector.css("backgroundColor", "#" + d({
        h: a.h,
                s: 100,
                b: 100
        })), t(e).data("colpick").selectorIndic.css({
        left: parseInt(t(e).data("colpick").height * a.s / 100, 10),
                top: parseInt(t(e).data("colpick").height * (100 - a.b) / 100, 10)
        })
        },
        p = function(a, e) {
        t(e).data("colpick").hue.css("top", parseInt(t(e).data("colpick").height - t(e).data("colpick").height * a.h / 360, 10))
        },
        h = function(a, e) {
        t(e).data("colpick").currentColor.css("backgroundColor", "#" + d(a))
        },
        u = function(a, e) {
        t(e).data("colpick").newColor.css("backgroundColor", "#" + d(a))
        },
        f = function(a) {
        var e, h = t(this).parent().parent();
                this.parentNode.className.indexOf("_hex") > 0 ? (h.data("colpick").color = e = i(L(this.value)), l(e, h.get(0)), r(e, h.get(0))) : this.parentNode.className.indexOf("_hsb") > 0 ? (h.data("colpick").color = e = X({
        h: parseInt(h.data("colpick").fields.eq(4).val(), 10),
                s: parseInt(h.data("colpick").fields.eq(5).val(), 10),
                b: parseInt(h.data("colpick").fields.eq(6).val(), 10)
        }), l(e, h.get(0)), n(e, h.get(0))) : (h.data("colpick").color = e = o(E({
        r: parseInt(h.data("colpick").fields.eq(1).val(), 10),
                g: parseInt(h.data("colpick").fields.eq(2).val(), 10),
                b: parseInt(h.data("colpick").fields.eq(3).val(), 10)
        })), n(e, h.get(0)), r(e, h.get(0))), s(e, h.get(0)), p(e, h.get(0)), u(e, h.get(0)), h.data("colpick").onChange.apply(h.parent(), [e, d(e), c(e), h.data("colpick").el, 0])
        },
        v = function(a) {
        t(this).parent().removeClass("colpick_focus")
        },
        g = function() {
        t(this).parent().parent().data("colpick").fields.parent().removeClass("colpick_focus"), t(this).parent().addClass("colpick_focus")
        },
        k = function(a) {
        a.preventDefault ? a.preventDefault() : a.returnValue = !1;
                var e = t(this).parent().find("input").focus(),
                i = {
                el: t(this).parent().addClass("colpick_slider"),
                        max: this.parentNode.className.indexOf("_hsb_h") > 0 ? 360 : this.parentNode.className.indexOf("_hsb") > 0 ? 100 : 255,
                        y: a.pageY,
                        field: e,
                        val: parseInt(e.val(), 10),
                        preview: t(this).parent().parent().data("colpick").livePreview
                };
                t(document).mouseup(i, m), t(document).mousemove(i, _)
        },
        _ = function(t) {
        return t.data.field.val(Math.max(0, Math.min(t.data.max, parseInt(t.data.val - t.pageY + t.data.y, 10)))), t.data.preview && f.apply(t.data.field.get(0), [!0]), !1
        },
        m = function(a) {
        return f.apply(a.data.field.get(0), [!0]), a.data.el.removeClass("colpick_slider").find("input").focus(), t(document).off("mouseup", m), t(document).off("mousemove", _), !1
        },
        b = function(a) {
        a.preventDefault ? a.preventDefault() : a.returnValue = !1;
                var e = {
                cal: t(this).parent(),
                        y: t(this).offset().top
                };
                t(document).on("mouseup touchend", e, y), t(document).on("mousemove touchmove", e, x);
                var i = "touchstart" == a.type ? a.originalEvent.changedTouches[0].pageY : a.pageY;
                return f.apply(e.cal.data("colpick").fields.eq(4).val(parseInt(360 * (e.cal.data("colpick").height - (i - e.y)) / e.cal.data("colpick").height, 10)).get(0), [e.cal.data("colpick").livePreview]), !1
        },
        x = function(t) {
        var a = "touchmove" == t.type ? t.originalEvent.changedTouches[0].pageY : t.pageY;
                return f.apply(t.data.cal.data("colpick").fields.eq(4).val(parseInt(360 * (t.data.cal.data("colpick").height - Math.max(0, Math.min(t.data.cal.data("colpick").height, a - t.data.y))) / t.data.cal.data("colpick").height, 10)).get(0), [t.data.preview]), !1
        },
        y = function(a) {
        return l(a.data.cal.data("colpick").color, a.data.cal.get(0)), n(a.data.cal.data("colpick").color, a.data.cal.get(0)), t(document).off("mouseup touchend", y), t(document).off("mousemove touchmove", x), !1
        },
        w = function(a) {
        a.preventDefault ? a.preventDefault() : a.returnValue = !1;
                var e = {
                cal: t(this).parent(),
                        pos: t(this).offset()
                };
                e.preview = e.cal.data("colpick").livePreview, t(document).on("mouseup touchend", e, I), t(document).on("mousemove touchmove", e, M);
                var i;
                return "touchstart" == a.type ? (pageX = a.originalEvent.changedTouches[0].pageX, i = a.originalEvent.changedTouches[0].pageY) : (pageX = a.pageX, i = a.pageY), f.apply(e.cal.data("colpick").fields.eq(6).val(parseInt(100 * (e.cal.data("colpick").height - (i - e.pos.top)) / e.cal.data("colpick").height, 10)).end().eq(5).val(parseInt(100 * (pageX - e.pos.left) / e.cal.data("colpick").height, 10)).get(0), [e.preview]), !1
        },
        M = function(t) {
        var a;
                return "touchmove" == t.type ? (pageX = t.originalEvent.changedTouches[0].pageX, a = t.originalEvent.changedTouches[0].pageY) : (pageX = t.pageX, a = t.pageY), f.apply(t.data.cal.data("colpick").fields.eq(6).val(parseInt(100 * (t.data.cal.data("colpick").height - Math.max(0, Math.min(t.data.cal.data("colpick").height, a - t.data.pos.top))) / t.data.cal.data("colpick").height, 10)).end().eq(5).val(parseInt(100 * Math.max(0, Math.min(t.data.cal.data("colpick").height, pageX - t.data.pos.left)) / t.data.cal.data("colpick").height, 10)).get(0), [t.data.preview]), !1
        },
        I = function(a) {
        return l(a.data.cal.data("colpick").color, a.data.cal.get(0)), n(a.data.cal.data("colpick").color, a.data.cal.get(0)), t(document).off("mouseup touchend", I), t(document).off("mousemove touchmove", M), !1
        },
        C = function(a) {
        var e = t(this).parent(),
                i = e.data("colpick").color;
                e.data("colpick").origColor = i, h(i, e.get(0)), e.data("colpick").onSubmit(i, d(i), c(i), e.data("colpick").el), t(e.get(0)).css("display", "none")
        },
        T = function(a) {
        a.stopPropagation();
                var e = t("#" + t(this).data("colpickId"));
                e.data("colpick").onBeforeShow.apply(this, [e.get(0)]);
                var i = t(this).offset(),
                o = i.top + this.offsetHeight,
                c = i.left,
                l = S(),
                d = e.width();
                c + d > l.l + l.w && (c -= d), e.css({
        left: c + "px",
                top: o + "px"
        }), 0 != e.data("colpick").onShow.apply(this, [e.get(0)]) && e.show(), t("html").mousedown({
        cal: e
        }, q), e.mousedown(function(t) {
        t.stopPropagation()
        })
        },
        q = function(a) {
        0 != a.data.cal.data("colpick").onHide.apply(this, [a.data.cal.get(0)]) && a.data.cal.hide(), t("html").off("mousedown", q)
        },
        S = function() {
        var t = "CSS1Compat" == document.compatMode;
                return {
                l: window.pageXOffset || (t ? document.documentElement.scrollLeft : document.body.scrollLeft),
                        w: window.innerWidth || (t ? document.documentElement.clientWidth : document.body.clientWidth)
                }
        },
        X = function(t) {
        return {
        h: Math.min(360, Math.max(0, t.h)),
                s: Math.min(100, Math.max(0, t.s)),
                b: Math.min(100, Math.max(0, t.b))
        }
        },
        E = function(t) {
        return {
        r: Math.min(255, Math.max(0, t.r)),
                g: Math.min(255, Math.max(0, t.g)),
                b: Math.min(255, Math.max(0, t.b))
        }
        },
        L = function(t) {
        var a = 6 - t.length;
                if (a > 0) {
        for (var e = [], i = 0; a > i; i++) e.push("0");
                e.push(t), t = e.join("")
        }
        return t
        },
        P = function() {
        var a = t(this).parent(),
                e = a.data("colpick").origColor;
                a.data("colpick").color = e, l(e, a.get(0)), n(e, a.get(0)), r(e, a.get(0)), s(e, a.get(0)), p(e, a.get(0)), u(e, a.get(0))
        };
        return {
        init: function(c) {
        if (c = t.extend({}, e, c || {}), "string" == typeof c.color) c.color = i(c.color);
                else if (void 0 != c.color.r && void 0 != c.color.g && void 0 != c.color.b) c.color = o(c.color);
                else {
                if (void 0 == c.color.h || void 0 == c.color.s || void 0 == c.color.b) return this;
                        c.color = X(c.color)
                }
        return this.each(function() {
        if (!t(this).data("colpickId")) {
        var e = t.extend({}, c);
                e.origColor = c.color;
                var i = "collorpicker_" + parseInt(1e3 * Math.random());
                t(this).data("colpickId", i);
                var o = t(a).attr("id", i);
                o.addClass("colpick_" + e.layout + (e.submit ? "" : " colpick_" + e.layout + "_ns")), "light" != e.colorScheme && o.addClass("colpick_" + e.colorScheme), o.find("div.colpick_submit").html(e.submitText).click(C), e.fields = o.find("input").change(f).blur(v).focus(g), o.find("div.colpick_field_arrs").mousedown(k).end().find("div.colpick_current_color").click(P), e.selector = o.find("div.colpick_color").on("mousedown touchstart", w), e.selectorIndic = e.selector.find("div.colpick_selector_outer"), e.el = this, e.hue = o.find("div.colpick_hue_arrs"), huebar = e.hue.parent();
                var d = navigator.userAgent.toLowerCase(),
                _ = "Microsoft Internet Explorer" === navigator.appName,
                m = _ ? parseFloat(d.match(/msie ([0-9]{1,}[\.0-9]{0,})/)[1]) : 0,
                x = _ && 10 > m,
                y = ["#ff0000", "#ff0080", "#ff00ff", "#8000ff", "#0000ff", "#0080ff", "#00ffff", "#00ff80", "#00ff00", "#80ff00", "#ffff00", "#ff8000", "#ff0000"];
                if (x) {
        var M, I;
                for (M = 0; 11 >= M; M++) I = t("<div></div>").attr("style", "height:8.333333%; filter:progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr=" + y[M] + ", endColorstr=" + y[M + 1] + '); -ms-filter: "progid:DXImageTransform.Microsoft.gradient(GradientType=0,startColorstr=' + y[M] + ", endColorstr=" + y[M + 1] + ')";'), huebar.append(I)
        } else stopList = y.join(","), huebar.attr("style", "background:-webkit-linear-gradient(top," + stopList + "); background: -o-linear-gradient(top," + stopList + "); background: -ms-linear-gradient(top," + stopList + "); background:-moz-linear-gradient(top," + stopList + "); -webkit-linear-gradient(top," + stopList + "); background:linear-gradient(to bottom," + stopList + "); ");
                o.find("div.colpick_hue").on("mousedown touchstart", b), e.newColor = o.find("div.colpick_new_color"), e.currentColor = o.find("div.colpick_current_color"), o.data("colpick", e), l(e.color, o.get(0)), r(e.color, o.get(0)), n(e.color, o.get(0)), p(e.color, o.get(0)), s(e.color, o.get(0)), h(e.color, o.get(0)), u(e.color, o.get(0)), e.flat ? (o.appendTo(this).show(), o.css({
        position: "relative",
                display: "block"
        })) : (o.appendTo(document.body), t(this).on(e.showEvent, T), o.css({
        position: "absolute"
        }))
        }
        })
        },
                showPicker: function() {
                return this.each(function() {
                t(this).data("colpickId") && T.apply(this)
                })
                },
                hidePicker: function() {
                return this.each(function() {
                t(this).data("colpickId") && t("#" + t(this).data("colpickId")).hide()
                })
                },
                setColor: function(a, e) {
                if (e = "undefined" == typeof e ? 1 : e, "string" == typeof a) a = i(a);
                        else if (void 0 != a.r && void 0 != a.g && void 0 != a.b) a = o(a);
                        else {
                        if (void 0 == a.h || void 0 == a.s || void 0 == a.b) return this;
                                a = X(a)
                        }
                return this.each(function() {
                if (t(this).data("colpickId")) {
                var i = t("#" + t(this).data("colpickId"));
                        i.data("colpick").color = a, i.data("colpick").origColor = a, l(a, i.get(0)), r(a, i.get(0)), n(a, i.get(0)), p(a, i.get(0)), s(a, i.get(0)), u(a, i.get(0)), i.data("colpick").onChange.apply(i.parent(), [a, d(a), c(a), i.data("colpick").el, 1]), e && h(a, i.get(0))
                }
                })
                }
        }
}(),
        e = function(t) {
        var t = parseInt(t.indexOf("#") > - 1 ? t.substring(1) : t, 16);
                return {
                r: t >> 16,
                        g: (65280 & t) >> 8,
                        b: 255 & t
                }
        },
        i = function(t) {
        return o(e(t))
        },
        o = function(t) {
        var a = {
        h: 0,
                s: 0,
                b: 0
        },
                e = Math.min(t.r, t.g, t.b),
                i = Math.max(t.r, t.g, t.b),
                o = i - e;
                return a.b = i, a.s = 0 != i ? 255 * o / i : 0, 0 != a.s ? t.r == i ? a.h = (t.g - t.b) / o : t.g == i ? a.h = 2 + (t.b - t.r) / o : a.h = 4 + (t.r - t.g) / o : a.h = - 1, a.h *= 60, a.h < 0 && (a.h += 360), a.s *= 100 / 255, a.b *= 100 / 255, a
        },
        c = function(t) {
        var a = {},
                e = t.h,
                i = 255 * t.s / 100,
                o = 255 * t.b / 100;
                if (0 == i) a.r = a.g = a.b = o;
                else {
                var c = o,
                        l = (255 - i) * o / 255,
                        d = (c - l) * (e % 60) / 60;
                        360 == e && (e = 0), 60 > e ? (a.r = c, a.b = l, a.g = l + d) : 120 > e ? (a.g = c, a.b = l, a.r = c - d) : 180 > e ? (a.g = c, a.r = l, a.b = l + d) : 240 > e ? (a.b = c, a.r = l, a.g = c - d) : 300 > e ? (a.b = c, a.g = l, a.r = l + d) : 360 > e ? (a.r = c, a.g = l, a.b = c - d) : (a.r = 0, a.g = 0, a.b = 0)
                }
        return {
        r: Math.round(a.r),
                g: Math.round(a.g),
                b: Math.round(a.b)
        }
        },
        l = function(a) {
        var e = [a.r.toString(16), a.g.toString(16), a.b.toString(16)];
                return t.each(e, function(t, a) {
                1 == a.length && (e[t] = "0" + a)
                }), e.join("")
        },
        d = function(t) {
        return l(c(t))
        };
        t.fn.extend({
        colpick: a.init,
                colpickHide: a.hidePicker,
                colpickShow: a.showPicker,
                colpickSetColor: a.setColor
        }), t.extend({
colpick: {
rgbToHex: l,
        rgbToHsb: o,
        hsbToHex: d,
        hsbToRgb: c,
        hexToHsb: i,
        hexToRgb: e
        }
})
}(jQuery);