!function (t) {
   "function" === typeof define && define.amd ? define(["jquery", "datatables.net"], function (n) {
      return t(n, window, document);
   }) : "object" === typeof exports ? module.exports = function (n, e) {
      return n || (n = window), e && e.fn.dataTable || (e = require("datatables.net")(n, e).$), t(e, n, n.document);
   } : t(jQuery, window, document);
}(function (t, n, e, o) {
   var i = t.fn.dataTable,
           s = 0,
           r = 0,
           a = i.ext.buttons,
           u = function (n, e) {
              !0 === e && (e = {}), t.isArray(e) && (e = {
                 buttons: e
              }), this.c = t.extend(!0, {}, u.defaults, e), e.buttons && (this.c.buttons = e.buttons), this.s = {
                 dt: new i.Api(n),
                 buttons: [],
                 subButtons: [],
                 listenKeys: "",
                 namespace: "dtb" + s++
              }, this.dom = {
                 container: t("<" + this.c.dom.container.tag + "/>").addClass(this.c.dom.container.className)
              }, this._constructor();
           };
   t.extend(u.prototype, {
      action: function (t, n) {
         var e = this._indexToButton(t).conf;
         return n === o ? e.action : (e.action = n, this);
      },
      active: function (t, n) {
         var e = this._indexToButton(t),
                 i = this.c.dom.button.active;
         return n === o ? e.node.hasClass(i) : (e.node.toggleClass(i, n === o ? !0 : n), this);
      },
      add: function (t, n) {
         if ("string" === typeof t && -1 !== t.indexOf("-")) {
            var e = t.split("-");
            this.c.buttons[1 * e[0]].buttons.splice(1 * e[1], 0, n);
         } else
            this.c.buttons.splice(1 * t, 0, n);
         return this.dom.container.empty(), this._buildButtons(this.c.buttons), this;
      },
      container: function () {
         return this.dom.container;
      },
      disable: function (t) {
         return this._indexToButton(t).node.addClass(this.c.dom.button.disabled), this;
      },
      destroy: function () {
         t("body").off("keyup." + this.s.namespace);
         var n, e, o, i = this.s.buttons,
                 s = this.s.subButtons;
         for (n = 0, i = i.length; i > n; n++)
            for (this.removePrep(n), e = 0, o = s[n].length; o > e; e++)
               this.removePrep(n + "-" + e);
         for (this.removeCommit(), this.dom.container.remove(), s = this.s.dt.settings()[0], n = 0, i = s.length; i > n; n++)
            if (s.inst === this) {
               s.splice(n, 1);
               break
            }
         return this;
      },
      enable: function (t, n) {
         return !1 === n ? this.disable(t) : (this._indexToButton(t).node.removeClass(this.c.dom.button.disabled), this);
      },
      name: function () {
         return this.c.name;
      },
      node: function (t) {
         return this._indexToButton(t).node;
      },
      removeCommit: function () {
         var t, n, e = this.s.buttons,
                 o = this.s.subButtons;
         for (t = e.length - 1; t >= 0; t--)
            null === e[t] && (e.splice(t, 1), o.splice(t, 1), this.c.buttons.splice(t, 1));
         for (t = 0, e = o.length; e > t; t++)
            for (n = o[t].length - 1; n >= 0; n--)
               null === o[t][n] && (o[t].splice(n, 1), this.c.buttons[t].buttons.splice(n, 1));
         return this;
      },
      removePrep: function (t) {
         var n, e = this.s.dt;
         if ("number" == typeof t || -1 === t.indexOf("-"))
            n = this.s.buttons[1 * t], n.conf.destroy && n.conf.destroy.call(e.button(t), e, n, n.conf), n.node.remove(), this._removeKey(n.conf), this.s.buttons[1 * t] = null;
         else {
            var o = t.split("-");
            n = this.s.subButtons[1 * o[0]][1 * o[1]], n.conf.destroy && n.conf.destroy.call(e.button(t), e, n, n.conf), n.node.remove(), this._removeKey(n.conf), this.s.subButtons[1 * o[0]][1 * o[1]] = null;
         }
         return this;
      },
      text: function (t, n) {
         var e = this._indexToButton(t),
                 i = this.c.dom.collection.buttonLiner,
                 i = "string" === typeof t && -1 !== t.indexOf("-") && i && i.tag ? i.tag : this.c.dom.buttonLiner.tag,
                 s = this.s.dt,
                 r = function (t) {
                    return "function" === typeof t ? t(s, e.node, e.conf) : t;
                 };
         return n === o ? r(e.conf.text) : (e.conf.text = n, i ? e.node.children(i).html(r(n)) : e.node.html(r(n)), this);
      },
      toIndex: function (t) {
         var n, e, o, i;
         o = this.s.buttons;
         var s = this.s.subButtons;
         for (n = 0, e = o.length; e > n; n++)
            if (o[n].node[0] === t)
               return n + "";
         for (n = 0, e = s.length; e > n; n++)
            for (o = 0, i = s[n].length; i > o; o++)
               if (s[n][o].node[0] === t)
                  return n + "-" + o;
      },
      _constructor: function () {
         var n = this,
                 o = this.s.dt,
                 i = o.settings()[0];
         i._buttons || (i._buttons = []), i._buttons.push({
            inst: this,
            name: this.c.name
         }), this._buildButtons(this.c.buttons), o.on("destroy", function () {
            n.destroy();
         }), t("body").on("keyup." + this.s.namespace, function (t) {
            if (!e.activeElement || e.activeElement === e.body) {
               var o = String.fromCharCode(t.keyCode).toLowerCase();
               -1 !== n.s.listenKeys.toLowerCase().indexOf(o) && n._keypress(o, t);
            }
         });
      },
      _addKey: function (n) {
         n.key && (this.s.listenKeys += t.isPlainObject(n.key) ? n.key.key : n.key);
      },
      _buildButtons: function (n, e, i) {
         var s = this.s.dt,
                 r = 0;
         e || (e = this.dom.container, this.s.buttons = [], this.s.subButtons = []);
         for (var a = 0, u = n.length; u > a; a++) {
            var c = this._resolveExtends(n[a]);
            if (c)
               if (t.isArray(c))
                  this._buildButtons(c, e, i);
               else {
                  var l = this._buildButton(c, i !== o ? !0 : !1);
                  if (l) {
                     var d = l.node;
                     e.append(l.inserter), i === o ? (this.s.buttons.push({
                        node: d,
                        conf: c,
                        inserter: l.inserter
                     }), this.s.subButtons.push([])) : this.s.subButtons[i].push({
                        node: d,
                        conf: c,
                        inserter: l.inserter
                     }), c.buttons && (l = this.c.dom.collection, c._collection = t("<" + l.tag + "/>").addClass(l.className), this._buildButtons(c.buttons, c._collection, r)), c.init && c.init.call(s.button(d), s, d, c), r++;
                  }
               }
         }
      },
      _buildButton: function (n, e) {
         var o = this.c.dom.button,
                 i = this.c.dom.buttonLiner,
                 s = this.c.dom.collection,
                 a = this.s.dt,
                 u = function (t) {
                    return "function" == typeof t ? t(a, l, n) : t;
                 };
         if (e && s.button && (o = s.button), e && s.buttonLiner && (i = s.buttonLiner), n.available && !n.available(a, n))
            return !1;
         var c = function (n, e, o, i) {
            i.action.call(e.button(o), n, e, o, i), t(e.table().node()).triggerHandler("buttons-action.dt", [e.button(o), e, o, i]);
         },
                 l = t("<" + o.tag + "/>").addClass(o.className).attr("tabindex", this.s.dt.settings()[0].iTabIndex).attr("aria-controls", this.s.dt.table().node().id).on("click.dtb", function (t) {
            t.preventDefault(), !l.hasClass(o.disabled) && n.action && c(t, a, l, n), l.blur();
         }).on("keyup.dtb", function (t) {
            13 === t.keyCode && !l.hasClass(o.disabled) && n.action && c(t, a, l, n);
         });
         return i.tag ? l.append(t("<" + i.tag + "/>").html(u(n.text)).addClass(i.className)) : l.html(u(n.text)), !1 === n.enabled && l.addClass(o.disabled), n.className && l.addClass(n.className), n.titleAttr && l.attr("title", n.titleAttr), n.namespace || (n.namespace = ".dt-button-" + r++), i = (i = this.c.dom.buttonContainer) && i.tag ? t("<" + i.tag + "/>").addClass(i.className).append(l) : l, this._addKey(n), {
            node: l,
            inserter: i
         };
      },
      _indexToButton: function (t) {
         return "number" === typeof t || -1 === t.indexOf("-") ? this.s.buttons[1 * t] : (t = t.split("-"), this.s.subButtons[1 * t[0]][1 * t[1]]);
      },
      _keypress: function (n, e) {
         var o, i, s, r;
         s = this.s.buttons;
         var a = this.s.subButtons,
                 u = function (o, i) {
                    o.key && (o.key === n ? i.click() : !t.isPlainObject(o.key) || o.key.key !== n || o.key.shiftKey && !e.shiftKey || (!o.key.altKey || e.altKey) && (!o.key.ctrlKey || e.ctrlKey) && (!o.key.metaKey || e.metaKey) && i.click());
                 };
         for (o = 0, i = s.length; i > o; o++)
            u(s[o].conf, s[o].node);
         for (o = 0, i = a.length; i > o; o++)
            for (s = 0, r = a[o].length; r > s; s++)
               u(a[o][s].conf, a[o][s].node);
      },
      _removeKey: function (n) {
         if (n.key) {
            var e = t.isPlainObject(n.key) ? n.key.key : n.key,
                    n = this.s.listenKeys.split(""),
                    e = t.inArray(e, n);
            n.splice(e, 1), this.s.listenKeys = n.join("");
         }
      },
      _resolveExtends: function (n) {
         for (var e, i, s = this.s.dt, r = function (e) {
            for (var i = 0; !t.isPlainObject(e) && !t.isArray(e); ) {
               if (e === o)
                  return;
               if ("function" === typeof e) {
                  if (e = e(s, n), !e)
                     return !1;
               } else if ("string" === typeof e) {
                  if (!a[e])
                     throw "Unknown button type: " + e;
                  e = a[e];
               }
               if (i++, i > 30)
                  throw "Buttons: Too many iterations";
            }
            return t.isArray(e) ? e : t.extend({}, e);
         }, n = r(n); n && n.extend; ) {
            if (!a[n.extend])
               throw "Cannot extend unknown button type: " + n.extend;
            var u = r(a[n.extend]);
            if (t.isArray(u))
               return u;
            if (!u)
               return !1;
            e = u.className, n = t.extend({}, u, n), e && n.className !== e && (n.className = e + " " + n.className);
            var c = n.postfixButtons;
            if (c) {
               for (n.buttons || (n.buttons = []), e = 0, i = c.length; i > e; e++)
                  n.buttons.push(c[e]);
               n.postfixButtons = null;
            }
            if (c = n.prefixButtons) {
               for (n.buttons || (n.buttons = []), e = 0, i = c.length; i > e; e++)
                  n.buttons.splice(e, 0, c[e]);
               n.prefixButtons = null;
            }
            n.extend = u.extend;
         }
         return n;
      }
   }), u.background = function (n, e, i) {
      i === o && (i = 400), n ? t("<div/>").addClass(e).css("display", "none").appendTo("body").fadeIn(i) : t("body > div." + e).fadeOut(i, function () {
         t(this).remove();
      });
   }, u.instanceSelector = function (n, e) {
      if (!n)
         return t.map(e, function (t) {
            return t.inst;
         });
      var o = [],
              i = t.map(e, function (t) {
                 return t.name;
              }),
              s = function (n) {
                 if (t.isArray(n))
                    for (var r = 0, a = n.length; a > r; r++)
                       s(n[r]);
                 else
                    "string" === typeof n ? -1 !== n.indexOf(",") ? s(n.split(",")) : (n = t.inArray(t.trim(n), i), -1 !== n && o.push(e[n].inst)) : "number" === typeof n && o.push(e[n].inst);
              };
      return s(n), o;
   }, u.buttonSelector = function (n, e) {
      for (var i = [], s = function (n, e) {
         var r, a, u = [];
         if (t.each(e.s.buttons, function (t, n) {
            null !== n && u.push({
               node: n.node[0],
               name: n.conf.name
            });
         }), t.each(e.s.subButtons, function (n, e) {
            t.each(e, function (t, n) {
               null !== n && u.push({
                  node: n.node[0],
                  name: n.conf.name
               });
            });
         }), r = t.map(u, function (t) {
            return t.node;
         }), t.isArray(n) || n instanceof t)
            for (r = 0, a = n.length; a > r; r++)
               s(n[r], e);
         else if (null === n || n === o || "*" === n)
            for (r = 0, a = u.length; a > r; r++)
               i.push({
                  inst: e,
                  idx: e.toIndex(u[r].node)
               });
         else if ("number" === typeof n)
            i.push({
               inst: e,
               idx: n
            });
         else if ("string" === typeof n)
            if (-1 !== n.indexOf(",")) {
               var c = n.split(",");
               for (r = 0, a = c.length; a > r; r++)
                  s(t.trim(c[r]), e);
            } else if (n.match(/^\d+(\-\d+)?$/))
               i.push({
                  inst: e,
                  idx: n
               });
            else if (-1 !== n.indexOf(":name"))
               for (c = n.replace(":name", ""), r = 0, a = u.length; a > r; r++)
                  u[r].name === c && i.push({
                     inst: e,
                     idx: e.toIndex(u[r].node)
                  });
            else
               t(r).filter(n).each(function () {
                  i.push({
                     inst: e,
                     idx: e.toIndex(this)
                  });
               });
         else
            "object" === typeof n && n.nodeName && (a = t.inArray(n, r), -1 !== a && i.push({
               inst: e,
               idx: e.toIndex(r[a])
            }));
      }, r = 0, a = n.length; a > r; r++)
         s(e, n[r]);
      return i;
   }, u.defaults = {
      buttons: ["copy", "excel", "csv", "pdf", "print"],
      name: "main",
      tabIndex: 0,
      dom: {
         container: {
            tag: "div",
            className: "dt-buttons"
         },
         collection: {
            tag: "div",
            className: "dt-button-collection"
         },
         button: {
            tag: "a",
            className: "dt-button",
            active: "active",
            disabled: "disabled"
         },
         buttonLiner: {
            tag: "span",
            className: ""
         }
      }
   }, u.version = "1.1.2", t.extend(a, {
      collection: {
         text: function (t) {
            return t.i18n("buttons.collection", "Collection");
         },
         className: "buttons-collection",
         action: function (o, i, s, r) {
            var o = s.offset(),
                    a = t(i.table().container()),
                    c = !1;
            t("div.dt-button-background").length && (c = t("div.dt-button-collection").offset(), t(e).trigger("click.dtb-collection")), r._collection.addClass(r.collectionLayout).css("display", "none").appendTo("body").fadeIn(r.fade);
            var l = r._collection.css("position");
            c && "absolute" === l ? r._collection.css({
               top: c.top + 5,
               left: c.left + 5
            }) : "absolute" === l ? (r._collection.css({
               top: o.top + s.outerHeight(),
               left: o.left
            }), s = o.left + r._collection.outerWidth(), a = a.offset().left + a.width(), s > a && r._collection.css("left", o.left - (s - a))) : (o = r._collection.height() / 2, o > t(n).height() / 2 && (o = t(n).height() / 2), r._collection.css("marginTop", -1 * o)), r.background && u.background(!0, r.backgroundClassName, r.fade), setTimeout(function () {
               t("div.dt-button-background").on("click.dtb-collection", function () {}), t("body").on("click.dtb-collection", function (n) {
                  t(n.target).parents().andSelf().filter(r._collection).length || (r._collection.fadeOut(r.fade, function () {
                     r._collection.detach();
                  }), t("div.dt-button-background").off("click.dtb-collection"), u.background(!1, r.backgroundClassName, r.fade), t("body").off("click.dtb-collection"), i.off("buttons-action.b-internal"));
               });
            }, 10), r.autoClose && i.on("buttons-action.b-internal", function () {
               t("div.dt-button-background").click();
            });
         },
         background: !0,
         collectionLayout: "",
         backgroundClassName: "dt-button-background",
         autoClose: !1,
         fade: 400
      },
      copy: function (t, n) {
         return a.copyHtml5 ? "copyHtml5" : a.copyFlash && a.copyFlash.available(t, n) ? "copyFlash" : void 0;
      },
      csv: function (t, n) {
         return a.csvHtml5 && a.csvHtml5.available(t, n) ? "csvHtml5" : a.csvFlash && a.csvFlash.available(t, n) ? "csvFlash" : void 0;
      },
      excel: function (t, n) {
         return a.excelHtml5 && a.excelHtml5.available(t, n) ? "excelHtml5" : a.excelFlash && a.excelFlash.available(t, n) ? "excelFlash" : void 0;
      },
      pdf: function (t, n) {
         return a.pdfHtml5 && a.pdfHtml5.available(t, n) ? "pdfHtml5" : a.pdfFlash && a.pdfFlash.available(t, n) ? "pdfFlash" : void 0;
      },
      pageLength: function (n) {
         var n = n.settings()[0].aLengthMenu,
                 e = t.isArray(n[0]) ? n[0] : n,
                 o = t.isArray(n[0]) ? n[1] : n,
                 i = function (t) {
                    return t.i18n("buttons.pageLength", {
                       "-1": "Show all rows",
                       _: "Show %d rows"
                    }, t.page.len());
                 };
         return {
            extend: "collection",
            text: i,
            className: "buttons-page-length",
            autoClose: !0,
            buttons: t.map(e, function (t, n) {
               return {
                  text: o[n],
                  action: function (n, e) {
                     e.page.len(t).draw();
                  },
                  init: function (n, e, o) {
                     var i = this,
                             e = function () {
                                i.active(n.page.len() === t);
                             };
                     n.on("length.dt" + o.namespace, e), e();
                  },
                  destroy: function (t, n, e) {
                     t.off("length.dt" + e.namespace);
                  }
               };
            }),
            init: function (t, n, e) {
               var o = this;
               t.on("length.dt" + e.namespace, function () {
                  o.text(i(t));
               });
            },
            destroy: function (t, n, e) {
               t.off("length.dt" + e.namespace);
            }
         };
      }
   }), i.Api.register("buttons()", function (t, n) {
      return n === o && (n = t, t = o), this.iterator(!0, "table", function (e) {
         return e._buttons ? u.buttonSelector(u.instanceSelector(t, e._buttons), n) : void 0;
      }, !0);
   }), i.Api.register("button()", function (t, n) {
      var e = this.buttons(t, n);
      return 1 < e.length && e.splice(1, e.length), e;
   }), i.Api.registerPlural("buttons().active()", "button().active()", function (t) {
      return t === o ? this.map(function (t) {
         return t.inst.active(t.idx);
      }) : this.each(function (n) {
         n.inst.active(n.idx, t);
      });
   }), i.Api.registerPlural("buttons().action()", "button().action()", function (t) {
      return t === o ? this.map(function (t) {
         return t.inst.action(t.idx);
      }) : this.each(function (n) {
         n.inst.action(n.idx, t);
      });
   }), i.Api.register(["buttons().enable()", "button().enable()"], function (t) {
      return this.each(function (n) {
         n.inst.enable(n.idx, t);
      });
   }), i.Api.register(["buttons().disable()", "button().disable()"], function () {
      return this.each(function (t) {
         t.inst.disable(t.idx);
      });
   }), i.Api.registerPlural("buttons().nodes()", "button().node()", function () {
      var n = t();
      return t(this.each(function (t) {
         n = n.add(t.inst.node(t.idx));
      })), n;
   }), i.Api.registerPlural("buttons().text()", "button().text()", function (t) {
      return t === o ? this.map(function (t) {
         return t.inst.text(t.idx);
      }) : this.each(function (n) {
         n.inst.text(n.idx, t);
      });
   }), i.Api.registerPlural("buttons().trigger()", "button().trigger()", function () {
      return this.each(function (t) {
         t.inst.node(t.idx).trigger("click");
      });
   }), i.Api.registerPlural("buttons().containers()", "buttons().container()", function () {
      var n = t();
      return t(this.each(function (t) {
         n = n.add(t.inst.container());
      })), n;
   }), i.Api.register("button().add()", function (t, n) {
      return 1 === this.length && this[0].inst.add(t, n), this.button(t);
   }), i.Api.register("buttons().destroy()", function () {
      return this.pluck("inst").unique().each(function (t) {
         t.destroy();
      }), this;
   }), i.Api.registerPlural("buttons().remove()", "buttons().remove()", function () {
      return this.each(function (t) {
         t.inst.removePrep(t.idx);
      }), this.pluck("inst").unique().each(function (t) {
         t.removeCommit();
      }), this;
   });
   var c;
   i.Api.register("buttons.info()", function (n, e, i) {
      var s = this;
      return !1 === n ? (t("#datatables_buttons_info").fadeOut(function () {
         t(this).remove();
      }), clearTimeout(c), c = null, this) : (c && clearTimeout(c), t("#datatables_buttons_info").length && t("#datatables_buttons_info").remove(), t('<div id="datatables_buttons_info" class="dt-button-info"/>').html(n ? "<h2>" + n + "</h2>" : "").append(t("<div/>")["string" === typeof e ? "html" : "append"](e)).css("display", "none").appendTo("body").fadeIn(), i !== o && 0 !== i && (c = setTimeout(function () {
         s.buttons.info(!1);
      }, i)), this);
   }), i.Api.register("buttons.exportData()", function (n) {
      if (this.context.length) {
         for (var e = new i.Api(this.context[0]), o = t.extend(!0, {}, {
            rows: null,
            columns: "",
            modifier: {
               search: "applied",
               order: "applied"
            },
            orthogonal: "display",
            stripHtml: !0,
            stripNewlines: !0,
            decodeEntities: !0,
            trim: !0,
            format: {
               header: function (t) {
                  return s(t);
               },
               footer: function (t) {
                  return s(t);
               },
               body: function (t) {
                  return s(t);
               }
            }
         }, n), s = function (t) {
            return "string" !== typeof t ? t : (o.stripHtml && (t = t.replace(/<.*?>/g, "")), o.trim && (t = t.replace(/^\s+|\s+$/g, "")), o.stripNewlines && (t = t.replace(/\n/g, " ")), o.decodeEntities && (l.innerHTML = t, t = l.value), t);
         }, n = e.columns(o.columns).indexes().map(function (t) {
            return o.format.header(e.column(t).header().innerHTML, t);
         }).toArray(), r = e.table().footer() ? e.columns(o.columns).indexes().map(function (t) {
            var n = e.column(t).footer();
            return o.format.footer(n ? n.innerHTML : "", t);
         }).toArray() : null, a = e.rows(o.rows, o.modifier).indexes().toArray(), a = e.cells(a, o.columns).render(o.orthogonal).toArray(), u = n.length, c = u > 0 ? a.length / u : 0, d = Array(c), f = 0, h = 0; c > h; h++) {
            for (var b = Array(u), p = 0; u > p; p++)
               b[p] = o.format.body(a[f], p, h), f++;
            d[h] = b;
         }
         return {
            header: n,
            footer: r,
            body: d
         };
      }
   });
   var l = t("<textarea/>")[0];
   return t.fn.dataTable.Buttons = u, t.fn.DataTable.Buttons = u, t(e).on("init.dt plugin-init.dt", function (t, n) {
      if ("dt" === t.namespace) {
         var e = n.oInit.buttons || i.defaults.buttons;
         e && !n._buttons && new u(n, e).container();
      }
   }), i.ext.feature.push({
      fnInit: function (t) {
         var t = new i.Api(t),
                 n = t.init().buttons || i.defaults.buttons;
         return new u(t, n).container();
      },
      cFeature: "B"
   }), u;
});