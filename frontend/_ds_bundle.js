/* @ds-bundle: {"format":3,"namespace":"SDCMetadataDesignSystem_967a78","components":[{"name":"Button","sourcePath":"components/actions/Button.jsx"},{"name":"Card","sourcePath":"components/data/Card.jsx"},{"name":"Stepper","sourcePath":"components/data/Stepper.jsx"},{"name":"Table","sourcePath":"components/data/Table.jsx"},{"name":"Alert","sourcePath":"components/feedback/Alert.jsx"},{"name":"Badge","sourcePath":"components/feedback/Badge.jsx"},{"name":"Tag","sourcePath":"components/feedback/Badge.jsx"},{"name":"FileUpload","sourcePath":"components/forms/FileUpload.jsx"},{"name":"Input","sourcePath":"components/forms/Input.jsx"}],"sourceHashes":{"components/actions/Button.jsx":"ffecf9c2320e","components/data/Card.jsx":"e99ab208d840","components/data/Stepper.jsx":"e3e8bfe5c194","components/data/Table.jsx":"ec0fccf2b63e","components/feedback/Alert.jsx":"71f9ed2c8ea6","components/feedback/Badge.jsx":"87713d693297","components/forms/FileUpload.jsx":"366e0207b16e","components/forms/Input.jsx":"36cfa177e908","ui_kits/sdc-pipeline/App.jsx":"0c42a61b254f","ui_kits/sdc-pipeline/Shell.jsx":"042dbb22982a","ui_kits/sdc-pipeline/StepDepot.jsx":"aa1a9f62c182","ui_kits/sdc-pipeline/StepExport.jsx":"ee9e7ea2ecad","ui_kits/sdc-pipeline/StepQuestions.jsx":"4f28600885b5","ui_kits/sdc-pipeline/StepVerification.jsx":"ed8b11aefe7a","ui_kits/sdc-pipeline/data.js":"b57118c69e6b"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.SDCMetadataDesignSystem_967a78 = window.SDCMetadataDesignSystem_967a78 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/actions/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* DSFR Button — square corners, Bleu France primary, hover/active/focus states. */
const CSS = `
.ds-btn{
  --_bg: var(--background-action-high);
  --_bg-h: var(--background-action-high-hover);
  --_bg-a: var(--background-action-high-active);
  --_fg: var(--text-inverted);
  display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
  font-family:var(--font-sans);font-weight:var(--fw-medium);font-size:var(--text-md);
  line-height:1.5rem;border:1px solid transparent;border-radius:var(--radius-none);
  padding:.5rem 1.5rem;min-height:2.5rem;cursor:pointer;text-decoration:none;
  background:var(--_bg);color:var(--_fg);transition:background-color .12s ease, color .12s ease;
  white-space:nowrap;
}
.ds-btn:hover{background:var(--_bg-h);}
.ds-btn:active{background:var(--_bg-a);}
.ds-btn:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
.ds-btn[disabled]{cursor:not-allowed;background:var(--background-disabled);color:var(--text-disabled);}
.ds-btn--secondary{--_bg:transparent;--_fg:var(--text-action-high);border-color:var(--border-action-high);}
.ds-btn--secondary:hover{--_bg:var(--background-action-low);background:var(--background-action-low);}
.ds-btn--secondary:active{background:var(--background-action-low-active);}
.ds-btn--secondary[disabled]{background:transparent;border-color:var(--border-disabled);color:var(--text-disabled);}
.ds-btn--tertiary{--_bg:transparent;--_fg:var(--text-action-high);}
.ds-btn--tertiary:hover{background:var(--background-action-low);}
.ds-btn--tertiary--noborder{box-shadow:none;}
.ds-btn--tertiary:not(.ds-btn--tertiary--noborder){border-color:var(--border-default);}
.ds-btn--danger{--_bg:var(--background-flat-error);--_bg-h:#ff2725;--_bg-a:#ff4140;--_fg:#fff;}
.ds-btn--sm{font-size:var(--text-sm);padding:.25rem 1rem;min-height:2rem;}
.ds-btn--lg{font-size:var(--text-lg);padding:.75rem 2rem;min-height:3rem;}
.ds-btn--block{width:100%;}
.ds-btn > i{font-size:1.25em;line-height:1;}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-btn-css")) {
  const s = document.createElement("style");
  s.id = "ds-btn-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
function Button({
  children,
  variant = "primary",
  size = "md",
  icon,
  iconRight = false,
  block = false,
  as = "button",
  className = "",
  ...rest
}) {
  const cls = ["ds-btn", variant !== "primary" && `ds-btn--${variant}`, size !== "md" && `ds-btn--${size}`, block && "ds-btn--block", className].filter(Boolean).join(" ");
  const Tag = as;
  const ico = icon ? /*#__PURE__*/React.createElement("i", {
    className: icon,
    "aria-hidden": "true"
  }) : null;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: cls
  }, rest), !iconRight && ico, children, iconRight && ico);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/actions/Button.jsx", error: String((e && e.message) || e) }); }

// components/data/Card.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* DSFR card — square corners, hairline border, optional Bleu France bottom accent that
   thickens on hover, optional pictogram / badge / footer. */
const CSS = `
.ds-card{
  display:flex;flex-direction:column;font-family:var(--font-sans);
  background:var(--background-default);border:1px solid var(--border-default);
  border-radius:var(--radius-md);overflow:hidden;position:relative;
  box-shadow:inset 0 -.25rem 0 0 var(--background-action-high);
}
.ds-card--flat{box-shadow:none;}
.ds-card--raised{box-shadow:var(--shadow-raised), inset 0 -.25rem 0 0 var(--background-action-high);}
a.ds-card,button.ds-card{cursor:pointer;text-align:left;text-decoration:none;transition:box-shadow .12s ease, background-color .12s ease;}
a.ds-card:hover,button.ds-card:hover{background:var(--background-alt);box-shadow:var(--shadow-raised), inset 0 -.375rem 0 0 var(--background-action-high);}
a.ds-card:focus-visible,button.ds-card:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
.ds-card__body{display:flex;flex-direction:column;gap:.5rem;padding:1.5rem;flex:1;}
.ds-card__head{display:flex;align-items:flex-start;justify-content:space-between;gap:1rem;}
.ds-card__pic{width:48px;height:48px;flex:none;}
.ds-card__title{font-size:var(--h6);font-weight:var(--fw-bold);color:var(--text-title);line-height:1.75rem;margin:0;}
.ds-card__desc{font-size:var(--text-sm);color:var(--text-default);line-height:1.5rem;margin:0;}
.ds-card__foot{margin-top:auto;padding-top:.75rem;font-size:var(--text-sm);color:var(--text-mention);}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-card-css")) {
  const s = document.createElement("style");
  s.id = "ds-card-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
function Card({
  title,
  children,
  badge,
  pictogramSrc,
  footer,
  elevation = "accent",
  as = "div",
  className = "",
  ...rest
}) {
  const cls = ["ds-card", elevation === "flat" && "ds-card--flat", elevation === "raised" && "ds-card--raised", className].filter(Boolean).join(" ");
  const Tag = as;
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: cls
  }, rest), /*#__PURE__*/React.createElement("div", {
    className: "ds-card__body"
  }, /*#__PURE__*/React.createElement("div", {
    className: "ds-card__head"
  }, title && /*#__PURE__*/React.createElement("h3", {
    className: "ds-card__title"
  }, title), pictogramSrc && /*#__PURE__*/React.createElement("img", {
    className: "ds-card__pic",
    src: pictogramSrc,
    alt: "",
    "aria-hidden": "true"
  }), badge && !pictogramSrc && /*#__PURE__*/React.createElement("span", null, badge)), children && /*#__PURE__*/React.createElement("div", {
    className: "ds-card__desc"
  }, children), footer && /*#__PURE__*/React.createElement("div", {
    className: "ds-card__foot"
  }, footer)));
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Card.jsx", error: String((e && e.message) || e) }); }

// components/data/Stepper.jsx
try { (() => {
/* DSFR stepper — segmented progress, "Étape N sur M", current title, next-step hint. */
const CSS = `
.ds-stepper{font-family:var(--font-sans);display:flex;flex-direction:column;gap:.75rem;}
.ds-stepper__segments{display:flex;gap:.5rem;}
.ds-stepper__seg{height:.5rem;flex:1;background:var(--background-contrast);border-radius:var(--radius-pill);overflow:hidden;}
.ds-stepper__seg--done{background:var(--background-action-high);}
.ds-stepper__seg--current{background:var(--background-contrast);position:relative;}
.ds-stepper__seg--current::before{content:"";position:absolute;inset:0;width:100%;background:var(--background-action-high);border-radius:var(--radius-pill);}
.ds-stepper__count{font-size:var(--text-xs);font-weight:var(--fw-bold);color:var(--text-mention);text-transform:uppercase;letter-spacing:.03em;}
.ds-stepper__title{font-size:var(--h4);font-weight:var(--fw-bold);color:var(--text-title);line-height:2rem;margin:0;}
.ds-stepper__next{font-size:var(--text-sm);color:var(--text-mention);}
.ds-stepper__next b{font-weight:var(--fw-bold);color:var(--text-default);}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-stepper-css")) {
  const s = document.createElement("style");
  s.id = "ds-stepper-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
function Stepper({
  steps = [],
  current = 0,
  className = ""
}) {
  const total = steps.length;
  const next = steps[current + 1];
  return /*#__PURE__*/React.createElement("div", {
    className: ["ds-stepper", className].filter(Boolean).join(" ")
  }, /*#__PURE__*/React.createElement("div", {
    className: "ds-stepper__segments",
    "aria-hidden": "true"
  }, steps.map((_, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    className: "ds-stepper__seg " + (i < current ? "ds-stepper__seg--done" : i === current ? "ds-stepper__seg--current" : "")
  }))), /*#__PURE__*/React.createElement("span", {
    className: "ds-stepper__count"
  }, "\xC9tape ", current + 1, " sur ", total), /*#__PURE__*/React.createElement("p", {
    className: "ds-stepper__title"
  }, steps[current]), next && /*#__PURE__*/React.createElement("span", {
    className: "ds-stepper__next"
  }, "\xC9tape suivante : ", /*#__PURE__*/React.createElement("b", null, next)));
}
Object.assign(__ds_scope, { Stepper });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Stepper.jsx", error: String((e && e.message) || e) }); }

// components/data/Table.jsx
try { (() => {
/* DSFR table — caption, bold header, hairline rows, hover, mono cells, "NA" sentinel styling. */
const CSS = `
.ds-table-wrap{font-family:var(--font-sans);border:1px solid var(--border-default);border-radius:var(--radius-md);overflow:hidden;}
.ds-table-scroll{overflow-x:auto;}
.ds-table{border-collapse:collapse;width:100%;font-size:var(--text-sm);}
.ds-table caption{text-align:left;font-size:var(--text-sm);color:var(--text-mention);padding:.75rem 1rem;background:var(--background-default);caption-side:top;}
.ds-table thead th{
  text-align:left;font-weight:var(--fw-bold);color:var(--text-title);background:var(--background-alt);
  padding:.75rem 1rem;white-space:nowrap;border-bottom:1px solid var(--border-default);
}
.ds-table tbody td{padding:.625rem 1rem;color:var(--text-default);border-bottom:1px solid var(--border-default);vertical-align:top;}
.ds-table tbody tr:last-child td{border-bottom:0;}
.ds-table--striped tbody tr:nth-child(even) td{background:var(--background-alt);}
.ds-table tbody tr:hover td{background:var(--background-action-low);}
.ds-table__mono{font-family:var(--font-mono);font-size:var(--text-sm);color:var(--text-title);}
.ds-table__na{font-family:var(--font-mono);font-size:var(--text-xs);color:var(--text-mention);background:var(--background-contrast);padding:.0625rem .375rem;border-radius:var(--radius-sm);}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-table-css")) {
  const s = document.createElement("style");
  s.id = "ds-table-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}

/** Renders a cell value; the literal "NA" sentinel gets its own muted treatment. */
function Cell({
  value,
  mono
}) {
  if (value === "NA") return /*#__PURE__*/React.createElement("span", {
    className: "ds-table__na"
  }, "NA");
  if (mono) return /*#__PURE__*/React.createElement("span", {
    className: "ds-table__mono"
  }, value);
  return /*#__PURE__*/React.createElement(React.Fragment, null, value);
}
function Table({
  columns = [],
  rows = [],
  caption,
  striped = false,
  className = ""
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: ["ds-table-wrap", className].filter(Boolean).join(" ")
  }, /*#__PURE__*/React.createElement("div", {
    className: "ds-table-scroll"
  }, /*#__PURE__*/React.createElement("table", {
    className: "ds-table" + (striped ? " ds-table--striped" : "")
  }, caption && /*#__PURE__*/React.createElement("caption", null, caption), /*#__PURE__*/React.createElement("thead", null, /*#__PURE__*/React.createElement("tr", null, columns.map(c => /*#__PURE__*/React.createElement("th", {
    key: c.key,
    style: c.width ? {
      width: c.width
    } : undefined
  }, c.label)))), /*#__PURE__*/React.createElement("tbody", null, rows.map((r, i) => /*#__PURE__*/React.createElement("tr", {
    key: i
  }, columns.map(c => /*#__PURE__*/React.createElement("td", {
    key: c.key
  }, c.render ? c.render(r[c.key], r) : /*#__PURE__*/React.createElement(Cell, {
    value: r[c.key],
    mono: c.mono
  })))))))));
}
Object.assign(__ds_scope, { Table });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/data/Table.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Alert.jsx
try { (() => {
/* DSFR alert (notice) — info / success / warning / error, with left rule, icon, title, close. */
const CSS = `
.ds-alert{
  --_c: var(--border-plain-info);--_bg: var(--background-alt-info);--_tx: var(--text-default-info);
  position:relative;display:flex;gap:.75rem;font-family:var(--font-sans);
  background:var(--_bg);box-shadow:inset .25rem 0 0 0 var(--_c);
  padding:1rem 1rem 1rem 1.25rem;border-radius:0 var(--radius-md) var(--radius-md) 0;
}
.ds-alert--success{--_c:var(--border-plain-success);--_bg:var(--background-alt-success);--_tx:var(--text-default-success);}
.ds-alert--warning{--_c:var(--border-plain-warning);--_bg:var(--background-alt-warning);--_tx:var(--text-default-warning);}
.ds-alert--error{--_c:var(--border-plain-error);--_bg:var(--background-alt-error);--_tx:var(--text-default-error);}
.ds-alert__icon{color:var(--_c);font-size:1.25rem;line-height:1.5rem;flex:none;}
.ds-alert__body{display:flex;flex-direction:column;gap:.25rem;flex:1;min-width:0;}
.ds-alert__title{font-size:var(--text-md);font-weight:var(--fw-bold);color:var(--text-title);line-height:1.5rem;}
.ds-alert__desc{font-size:var(--text-sm);color:var(--text-default);line-height:1.5rem;}
.ds-alert--sm .ds-alert__title{font-size:var(--text-sm);}
.ds-alert__close{
  border:0;background:transparent;color:var(--text-default);cursor:pointer;flex:none;
  font-size:1.125rem;line-height:1;padding:.125rem;border-radius:var(--radius-sm);
}
.ds-alert__close:hover{color:var(--text-title);}
.ds-alert__close:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-alert-css")) {
  const s = document.createElement("style");
  s.id = "ds-alert-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
const ICONS = {
  info: "ri-information-line",
  success: "ri-checkbox-circle-line",
  warning: "ri-alert-line",
  error: "ri-error-warning-line"
};
function Alert({
  type = "info",
  title,
  children,
  small = false,
  onClose,
  className = ""
}) {
  const cls = ["ds-alert", type !== "info" && `ds-alert--${type}`, small && "ds-alert--sm", className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("div", {
    className: cls,
    role: "alert"
  }, /*#__PURE__*/React.createElement("i", {
    className: `ds-alert__icon ${ICONS[type]}`,
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", {
    className: "ds-alert__body"
  }, title && /*#__PURE__*/React.createElement("p", {
    className: "ds-alert__title"
  }, title), children && /*#__PURE__*/React.createElement("div", {
    className: "ds-alert__desc"
  }, children)), onClose && /*#__PURE__*/React.createElement("button", {
    type: "button",
    className: "ds-alert__close",
    "aria-label": "Masquer le message",
    onClick: onClose
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-close-line",
    "aria-hidden": "true"
  })));
}
Object.assign(__ds_scope, { Alert });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Alert.jsx", error: String((e && e.message) || e) }); }

// components/feedback/Badge.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* DSFR badge — small status pill, system-tinted. And Tag — neutral pill, optionally interactive. */
const CSS = `
.ds-badge{
  display:inline-flex;align-items:center;gap:.25rem;font-family:var(--font-sans);
  font-size:var(--text-xs);font-weight:var(--fw-bold);line-height:1.25rem;
  text-transform:uppercase;letter-spacing:.02em;padding:.125rem .5rem;
  border-radius:var(--radius-pill);background:var(--c-grey-950);color:var(--text-title);white-space:nowrap;
}
.ds-badge--no-pill{border-radius:var(--radius-none);}
.ds-badge > i{font-size:.875rem;}
.ds-badge--info{background:var(--c-info-950);color:var(--text-default-info);}
.ds-badge--success{background:var(--c-success-950);color:var(--text-default-success);}
.ds-badge--warning{background:var(--c-warning-950);color:var(--text-default-warning);}
.ds-badge--error{background:var(--c-error-950);color:var(--text-default-error);}
.ds-badge--new{background:var(--background-action-low);color:var(--text-action-high);}

.ds-tag{
  display:inline-flex;align-items:center;gap:.375rem;font-family:var(--font-sans);
  font-size:var(--text-sm);font-weight:var(--fw-regular);line-height:1.5rem;
  padding:.25rem .75rem;border-radius:var(--radius-pill);border:0;
  background:var(--background-contrast);color:var(--text-title);white-space:nowrap;
}
.ds-tag > i{font-size:1rem;}
.ds-tag--clickable{cursor:pointer;transition:background-color .12s ease;}
.ds-tag--clickable:hover{background:var(--background-contrast-hover);}
.ds-tag--clickable:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
.ds-tag--selected{background:var(--background-action-high);color:var(--text-inverted);}
.ds-tag--selected:hover{background:var(--background-action-high-hover);}
.ds-tag--dismiss{cursor:pointer;}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-badge-css")) {
  const s = document.createElement("style");
  s.id = "ds-badge-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
function Badge({
  children,
  type = "neutral",
  icon,
  pill = true,
  className = ""
}) {
  const cls = ["ds-badge", type !== "neutral" && `ds-badge--${type}`, !pill && "ds-badge--no-pill", className].filter(Boolean).join(" ");
  return /*#__PURE__*/React.createElement("span", {
    className: cls
  }, icon && /*#__PURE__*/React.createElement("i", {
    className: icon,
    "aria-hidden": "true"
  }), children);
}
function Tag({
  children,
  icon,
  selected = false,
  onClick,
  onDismiss,
  className = ""
}) {
  const interactive = !!onClick;
  const cls = ["ds-tag", interactive && "ds-tag--clickable", selected && "ds-tag--selected", onDismiss && "ds-tag--dismiss", className].filter(Boolean).join(" ");
  const Tag = interactive ? "button" : "span";
  return /*#__PURE__*/React.createElement(Tag, _extends({
    className: cls,
    onClick: onClick
  }, interactive ? {
    type: "button"
  } : {}), icon && /*#__PURE__*/React.createElement("i", {
    className: icon,
    "aria-hidden": "true"
  }), children, onDismiss && /*#__PURE__*/React.createElement("i", {
    className: "ri-close-line",
    "aria-hidden": "true",
    onClick: e => {
      e.stopPropagation();
      onDismiss();
    }
  }));
}
Object.assign(__ds_scope, { Badge, Tag });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/feedback/Badge.jsx", error: String((e && e.message) || e) }); }

// components/forms/FileUpload.jsx
try { (() => {
/* DSFR-aligned dropzone — drag & drop a metadata workbook, with selected-file state. */
const CSS = `
.ds-drop{font-family:var(--font-sans);}
.ds-drop__zone{
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.75rem;
  text-align:center;padding:2.5rem 2rem;background:var(--background-default);
  border:2px dashed var(--border-default);border-radius:var(--radius-md);
  cursor:pointer;transition:background-color .12s ease, border-color .12s ease;
}
.ds-drop__zone:hover{background:var(--background-alt);border-color:var(--c-blue-france-main-525);}
.ds-drop__zone:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
.ds-drop--over .ds-drop__zone{background:var(--background-action-low);border-color:var(--border-action-high);border-style:solid;}
.ds-drop__pic{width:64px;height:64px;}
.ds-drop__title{font-size:var(--text-md);color:var(--text-title);}
.ds-drop__title b{font-weight:var(--fw-bold);color:var(--text-action-high);}
.ds-drop__hint{font-size:var(--text-xs);color:var(--text-mention);}
.ds-drop__input{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none;}
/* selected file */
.ds-drop__file{
  display:flex;align-items:center;gap:1rem;padding:1rem 1.25rem;
  background:var(--background-alt);border:1px solid var(--border-default);
  border-left:4px solid var(--border-action-high);border-radius:var(--radius-md);
}
.ds-drop__file i.ds-file-ico{font-size:2rem;color:var(--text-action-high);line-height:1;}
.ds-drop__file-meta{display:flex;flex-direction:column;gap:.125rem;min-width:0;flex:1;}
.ds-drop__file-name{font-size:var(--text-md);font-weight:var(--fw-medium);color:var(--text-title);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.ds-drop__file-size{font-size:var(--text-xs);color:var(--text-mention);}
.ds-drop__remove{
  border:0;background:transparent;color:var(--text-default);cursor:pointer;
  font-size:1.25rem;padding:.25rem;border-radius:var(--radius-sm);line-height:1;
}
.ds-drop__remove:hover{color:var(--text-default-error);background:var(--background-contrast-error);}
.ds-drop__remove:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-drop-css")) {
  const s = document.createElement("style");
  s.id = "ds-drop-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
function fmtSize(bytes) {
  if (bytes == null) return "";
  if (bytes < 1024) return `${bytes} o`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} Ko`;
  return `${(bytes / 1024 / 1024).toFixed(1)} Mo`;
}
function FileUpload({
  accept = ".ods,.xlsx,.csv",
  formatsLabel = "Formats acceptés : .ods, .xlsx, .csv",
  file = null,
  onSelect,
  onRemove,
  pictogram = "data-visualization.svg",
  pictogramSrc,
  className = ""
}) {
  const [over, setOver] = React.useState(false);
  const inputRef = React.useRef(null);
  const picSrc = pictogramSrc || `../../assets/pictograms/${pictogram}`;
  const pick = f => f && onSelect && onSelect(f);
  if (file) {
    return /*#__PURE__*/React.createElement("div", {
      className: ["ds-drop", className].filter(Boolean).join(" ")
    }, /*#__PURE__*/React.createElement("div", {
      className: "ds-drop__file"
    }, /*#__PURE__*/React.createElement("i", {
      className: "ri-file-excel-2-line ds-file-ico",
      "aria-hidden": "true"
    }), /*#__PURE__*/React.createElement("span", {
      className: "ds-drop__file-meta"
    }, /*#__PURE__*/React.createElement("span", {
      className: "ds-drop__file-name"
    }, file.name), /*#__PURE__*/React.createElement("span", {
      className: "ds-drop__file-size"
    }, fmtSize(file.size))), /*#__PURE__*/React.createElement("button", {
      type: "button",
      className: "ds-drop__remove",
      "aria-label": "Retirer le fichier",
      onClick: onRemove
    }, /*#__PURE__*/React.createElement("i", {
      className: "ri-close-line",
      "aria-hidden": "true"
    }))));
  }
  return /*#__PURE__*/React.createElement("div", {
    className: ["ds-drop", over && "ds-drop--over", className].filter(Boolean).join(" ")
  }, /*#__PURE__*/React.createElement("div", {
    className: "ds-drop__zone",
    role: "button",
    tabIndex: 0,
    onClick: () => inputRef.current && inputRef.current.click(),
    onKeyDown: e => (e.key === "Enter" || e.key === " ") && inputRef.current && inputRef.current.click(),
    onDragOver: e => {
      e.preventDefault();
      setOver(true);
    },
    onDragLeave: () => setOver(false),
    onDrop: e => {
      e.preventDefault();
      setOver(false);
      pick(e.dataTransfer.files && e.dataTransfer.files[0]);
    }
  }, /*#__PURE__*/React.createElement("img", {
    className: "ds-drop__pic",
    src: picSrc,
    alt: "",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("span", {
    className: "ds-drop__title"
  }, "Glissez votre classeur ici ou ", /*#__PURE__*/React.createElement("b", null, "parcourez vos fichiers")), /*#__PURE__*/React.createElement("span", {
    className: "ds-drop__hint"
  }, formatsLabel), /*#__PURE__*/React.createElement("input", {
    ref: inputRef,
    type: "file",
    className: "ds-drop__input",
    accept: accept,
    onChange: e => pick(e.target.files && e.target.files[0])
  })));
}
Object.assign(__ds_scope, { FileUpload });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/FileUpload.jsx", error: String((e && e.message) || e) }); }

// components/forms/Input.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* DSFR text input — contrast fill, 2px bottom rule, label + hint + error/success. */
const CSS = `
.ds-field{display:flex;flex-direction:column;gap:.5rem;font-family:var(--font-sans);}
.ds-field__label{font-size:var(--text-sm);font-weight:var(--fw-bold);color:var(--text-label);line-height:1.5rem;}
.ds-field__hint{font-size:var(--text-xs);color:var(--text-mention);line-height:1.25rem;margin-top:-.25rem;}
.ds-field__input{
  font-family:inherit;font-size:var(--text-md);line-height:1.5rem;color:var(--text-default);
  background:var(--background-contrast);border:0;border-radius:var(--radius-sm) var(--radius-sm) 0 0;
  box-shadow:inset 0 -2px 0 0 var(--border-plain);padding:.5rem 1rem;width:100%;min-height:2.5rem;
  transition:box-shadow .12s ease;
}
.ds-field__input::placeholder{color:var(--text-mention);}
.ds-field__input:hover{background:var(--background-contrast-hover);}
.ds-field__input:focus-visible{outline:2px solid var(--focus-ring);outline-offset:2px;}
.ds-field__input[disabled]{background:var(--background-disabled);color:var(--text-disabled);box-shadow:inset 0 -2px 0 0 var(--border-disabled);cursor:not-allowed;}
.ds-field--error .ds-field__input{box-shadow:inset 0 -2px 0 0 var(--border-plain-error);}
.ds-field--success .ds-field__input{box-shadow:inset 0 -2px 0 0 var(--border-plain-success);}
.ds-field__msg{display:flex;align-items:center;gap:.375rem;font-size:var(--text-sm);line-height:1.5rem;}
.ds-field--error .ds-field__msg{color:var(--text-default-error);}
.ds-field--success .ds-field__msg{color:var(--text-default-success);}
.ds-field__msg > i{font-size:1rem;}
.ds-field--textarea .ds-field__input{min-height:6rem;resize:vertical;}
`;
if (typeof document !== "undefined" && !document.getElementById("ds-field-css")) {
  const s = document.createElement("style");
  s.id = "ds-field-css";
  s.textContent = CSS;
  document.head.appendChild(s);
}
let _id = 0;
function Input({
  label,
  hint,
  error,
  success,
  multiline = false,
  id,
  className = "",
  ...rest
}) {
  const fid = id || `ds-input-${++_id}`;
  const state = error ? "error" : success ? "success" : null;
  const cls = ["ds-field", multiline && "ds-field--textarea", state && `ds-field--${state}`, className].filter(Boolean).join(" ");
  const Control = multiline ? "textarea" : "input";
  return /*#__PURE__*/React.createElement("div", {
    className: cls
  }, label && /*#__PURE__*/React.createElement("label", {
    className: "ds-field__label",
    htmlFor: fid
  }, label), hint && /*#__PURE__*/React.createElement("span", {
    className: "ds-field__hint"
  }, hint), /*#__PURE__*/React.createElement(Control, _extends({
    id: fid,
    className: "ds-field__input"
  }, rest)), error && /*#__PURE__*/React.createElement("span", {
    className: "ds-field__msg"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-error-warning-line",
    "aria-hidden": "true"
  }), error), success && !error && /*#__PURE__*/React.createElement("span", {
    className: "ds-field__msg"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-checkbox-circle-line",
    "aria-hidden": "true"
  }), success));
}
Object.assign(__ds_scope, { Input });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/Input.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/App.jsx
try { (() => {
/* App — orchestrates the four-phase pipeline as an interactive click-through. */
const ADS = window.SDCMetadataDesignSystem_967a78;
const {
  useState: useAppState
} = React;
const STEPS = ["Dépôt", "Questions", "Vérification", "Export"];
function Processing({
  label
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-processing"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sdc-spinner",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("p", {
    className: "sdc-processing__label"
  }, label), /*#__PURE__*/React.createElement("p", {
    className: "sdc-processing__sub"
  }, "temperature = 0 \xB7 appel au mod\xE8le Qwen sur SSP Cloud"));
}
function App() {
  const {
    SAMPLE_MARKDOWN,
    QUESTIONS,
    RECORDS
  } = window.SDC_DATA;
  const [step, setStep] = useAppState(0);
  const [file, setFile] = useAppState(null);
  const [answers, setAnswers] = useAppState({});
  const [processing, setProcessing] = useAppState(null);
  const run = (label, to) => {
    setProcessing(label);
    setTimeout(() => {
      setProcessing(null);
      setStep(to);
    }, 1400);
  };
  const reset = () => {
    setFile(null);
    setAnswers({});
    setStep(0);
  };
  return /*#__PURE__*/React.createElement(Layout, null, /*#__PURE__*/React.createElement("div", {
    className: "sdc-container"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-stepper-wrap"
  }, /*#__PURE__*/React.createElement(ADS.Stepper, {
    steps: STEPS,
    current: step
  })), processing ? /*#__PURE__*/React.createElement(Processing, {
    label: processing
  }) : step === 0 ? /*#__PURE__*/React.createElement(StepDepot, {
    file: file,
    onSelect: setFile,
    onRemove: () => setFile(null),
    onNext: () => run("Lecture du classeur et analyse des ambiguïtés…", 1)
  }) : step === 1 ? /*#__PURE__*/React.createElement(StepQuestions, {
    questions: QUESTIONS,
    answers: answers,
    onAnswer: (id, val) => setAnswers(a => ({
      ...a,
      [id]: val
    })),
    onBack: () => setStep(0),
    onNext: () => run("Application des réponses et production du JSON…", 2)
  }) : step === 2 ? /*#__PURE__*/React.createElement(StepVerification, {
    markdown: SAMPLE_MARKDOWN,
    records: RECORDS,
    onBack: () => setStep(1),
    onNext: () => setStep(3)
  }) : /*#__PURE__*/React.createElement(StepExport, {
    records: RECORDS,
    fileName: file ? file.name : "metadonnees.ods",
    onRestart: reset
  })));
}
window.App = App;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/App.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/Shell.jsx
try { (() => {
/* DSFR application shell — gov.fr header (Marianne block-mark + Insee service) and footer. */
const {
  useState
} = React;
function Header() {
  return /*#__PURE__*/React.createElement("header", {
    className: "sdc-header",
    role: "banner"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-header__inner"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-header__brand"
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo-insee.png",
    alt: "Insee \u2014 Mesurer pour comprendre",
    className: "sdc-insee-logo-img"
  }), /*#__PURE__*/React.createElement("div", {
    className: "sdc-header__sep",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", {
    className: "sdc-header__service"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sdc-header__service-name"
  }, "Analyse des m\xE9tadonn\xE9es"), /*#__PURE__*/React.createElement("span", {
    className: "sdc-header__service-tag"
  }, "Pr\xE9parer un classeur pour la pose du secret"))), /*#__PURE__*/React.createElement("nav", {
    className: "sdc-header__tools",
    "aria-label": "Outils"
  }, /*#__PURE__*/React.createElement("a", {
    href: "#",
    className: "sdc-header__tool"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-question-line",
    "aria-hidden": "true"
  }), "Aide"), /*#__PURE__*/React.createElement("a", {
    href: "#",
    className: "sdc-header__tool"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-account-circle-line",
    "aria-hidden": "true"
  }), "j.martin@insee.fr"))));
}
function Footer() {
  return /*#__PURE__*/React.createElement("footer", {
    className: "sdc-footer",
    role: "contentinfo"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-footer__top"
  }, /*#__PURE__*/React.createElement("img", {
    src: "../../assets/logo-insee.png",
    alt: "Insee",
    className: "sdc-insee-logo-img sdc-insee-logo-img--footer"
  }), /*#__PURE__*/React.createElement("p", {
    className: "sdc-footer__desc"
  }, "Outil interne de l'Insee pour normaliser les m\xE9tadonn\xE9es de tableaux statistiques avant la pose du secret via ", /*#__PURE__*/React.createElement("b", null, "rtauargus"), ".")), /*#__PURE__*/React.createElement("ul", {
    className: "sdc-footer__links"
  }, /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "insee.fr")), /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "data.gouv.fr")), /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "Documentation rtauargus")), /*#__PURE__*/React.createElement("li", null, /*#__PURE__*/React.createElement("a", {
    href: "#"
  }, "Code source"))), /*#__PURE__*/React.createElement("div", {
    className: "sdc-footer__bottom"
  }, /*#__PURE__*/React.createElement("span", null, "\xA9 Insee ", new Date().getFullYear()), /*#__PURE__*/React.createElement("span", null, "Accessibilit\xE9 : partiellement conforme"), /*#__PURE__*/React.createElement("span", null, "Mentions l\xE9gales"), /*#__PURE__*/React.createElement("span", null, "Donn\xE9es personnelles")));
}
function Layout({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-app"
  }, /*#__PURE__*/React.createElement("a", {
    href: "#contenu",
    className: "sdc-skiplink"
  }, "Aller au contenu"), /*#__PURE__*/React.createElement(Header, null), /*#__PURE__*/React.createElement("main", {
    id: "contenu",
    className: "sdc-main"
  }, children), /*#__PURE__*/React.createElement(Footer, null));
}
Object.assign(window, {
  Header,
  Footer,
  Layout
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/Shell.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/StepDepot.jsx
try { (() => {
/* Étape 1 — Dépôt du classeur de métadonnées. */
const {
  Button: DepotButton,
  FileUpload: DepotUpload,
  Alert: DepotAlert
} = window.SDCMetadataDesignSystem_967a78;
function StepDepot({
  file,
  onSelect,
  onRemove,
  onNext
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-step"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-step__intro"
  }, /*#__PURE__*/React.createElement("img", {
    className: "sdc-step__pic",
    src: "../../assets/pictograms/document-add.svg",
    alt: "",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    className: "sdc-h1"
  }, "D\xE9posez votre classeur de m\xE9tadonn\xE9es"), /*#__PURE__*/React.createElement("p", {
    className: "sdc-lead"
  }, "Glissez un fichier ", /*#__PURE__*/React.createElement("b", null, ".ods"), ", ", /*#__PURE__*/React.createElement("b", null, ".xlsx"), " ou ", /*#__PURE__*/React.createElement("b", null, ".csv"), " d\xE9crivant les tableaux statistiques demand\xE9s. Le mod\xE8le le lit, vous pose des questions si n\xE9cessaire, puis produit un tableau normalis\xE9 pr\xEAt pour la pose du secret."))), /*#__PURE__*/React.createElement(DepotUpload, {
    file: file,
    onSelect: onSelect,
    onRemove: onRemove,
    pictogramSrc: "../../assets/pictograms/data-visualization.svg"
  }), /*#__PURE__*/React.createElement(DepotAlert, {
    type: "warning",
    title: "Ne transmettez jamais d'informations sensibles ou confidentielles."
  }, "Ce formulaire est exclusivement r\xE9serv\xE9 aux m\xE9tadonn\xE9es d\xE9crivant des tableaux statistiques. V\xE9rifiez votre fichier avant de l'envoyer\xA0: il ne doit contenir aucune donn\xE9e individuelle, ni micro-donn\xE9e, ni information \xE0 caract\xE8re personnel."), /*#__PURE__*/React.createElement("div", {
    className: "sdc-actions"
  }, /*#__PURE__*/React.createElement(DepotButton, {
    icon: "ri-play-line",
    disabled: !file,
    onClick: onNext
  }, "Lancer l'analyse")));
}
window.StepDepot = StepDepot;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/StepDepot.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/StepExport.jsx
try { (() => {
/* Étape 4 — Export du tableau normalisé (.csv pour relecture, .rds pour rtauargus). */
const EDS = window.SDCMetadataDesignSystem_967a78;
function Stat({
  value,
  label
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-stat"
  }, /*#__PURE__*/React.createElement("span", {
    className: "sdc-stat__value"
  }, value), /*#__PURE__*/React.createElement("span", {
    className: "sdc-stat__label"
  }, label));
}
function StepExport({
  records,
  fileName,
  onRestart
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-step"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-step__intro"
  }, /*#__PURE__*/React.createElement("img", {
    className: "sdc-step__pic",
    src: "../../assets/pictograms/document-download.svg",
    alt: "",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    className: "sdc-h1"
  }, "Tableau pr\xEAt \xE0 l'export"), /*#__PURE__*/React.createElement("p", {
    className: "sdc-lead"
  }, "Le tableau normalis\xE9 est reproductible : m\xEAme classeur en entr\xE9e \u2192 m\xEAme sortie. T\xE9l\xE9chargez-le pour relecture ou pour la pose du secret."))), /*#__PURE__*/React.createElement(EDS.Alert, {
    type: "success",
    title: "Pipeline termin\xE9"
  }, records.length, " tableaux normalis\xE9s et valid\xE9s \xE0 partir de ", /*#__PURE__*/React.createElement("b", null, fileName), "."), /*#__PURE__*/React.createElement("div", {
    className: "sdc-stats"
  }, /*#__PURE__*/React.createElement(Stat, {
    value: records.length,
    label: "tableaux"
  }), /*#__PURE__*/React.createElement(Stat, {
    value: "6",
    label: "colonnes (2n+5)"
  }), /*#__PURE__*/React.createElement(Stat, {
    value: "0",
    label: "erreur de sch\xE9ma"
  }), /*#__PURE__*/React.createElement(Stat, {
    value: "100 %",
    label: "reproductible"
  })), /*#__PURE__*/React.createElement("div", {
    className: "sdc-export"
  }, /*#__PURE__*/React.createElement(EDS.Card, {
    title: "demande_normalisee.csv",
    pictogramSrc: "../../assets/pictograms/document-download.svg",
    footer: /*#__PURE__*/React.createElement(EDS.Button, {
      size: "sm",
      icon: "ri-download-line"
    }, "T\xE9l\xE9charger le .csv")
  }, "Tableau plat pour relecture humaine \u2014 convention \xAB NA \xBB vs vide."), /*#__PURE__*/React.createElement(EDS.Card, {
    title: "demande_normalisee.rds",
    pictogramSrc: "../../assets/pictograms/coding.svg",
    footer: /*#__PURE__*/React.createElement(EDS.Button, {
      size: "sm",
      variant: "secondary",
      icon: "ri-download-line"
    }, "T\xE9l\xE9charger le .rds")
  }, "Objet R pr\xEAt pour ", /*#__PURE__*/React.createElement("b", null, "rtauargus"), " \u2014 NA cod\xE9s en NA R.")), /*#__PURE__*/React.createElement("div", {
    className: "sdc-actions"
  }, /*#__PURE__*/React.createElement(EDS.Button, {
    variant: "tertiary",
    icon: "ri-restart-line",
    onClick: onRestart
  }, "Analyser un autre classeur")));
}
window.StepExport = StepExport;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/StepExport.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/StepQuestions.jsx
try { (() => {
/* Étape 2 — Questions du modèle (boucle humaine). */
const QDS = window.SDCMetadataDesignSystem_967a78;
const {
  useState: useQState
} = React;
function QuestionCard({
  q,
  value,
  onAnswer
}) {
  const [custom, setCustom] = useQState('');
  function handleCustomChange(e) {
    const v = e.target.value;
    setCustom(v);
    onAnswer(q.id, v || null);
  }
  function handleOption(opt) {
    setCustom('');
    onAnswer(q.id, opt);
  }
  const isCustomActive = value && !q.options.includes(value);
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-question"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-question__head"
  }, /*#__PURE__*/React.createElement(QDS.Badge, {
    type: "new"
  }, "Question ", q.id), /*#__PURE__*/React.createElement("span", {
    className: "sdc-question__cat"
  }, q.category)), /*#__PURE__*/React.createElement("p", {
    className: "sdc-question__text"
  }, q.text), /*#__PURE__*/React.createElement("p", {
    className: "sdc-question__ref"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-file-text-line",
    "aria-hidden": "true"
  }), q.ref), /*#__PURE__*/React.createElement("div", {
    className: "sdc-question__opts"
  }, q.options.map(opt => /*#__PURE__*/React.createElement(QDS.Tag, {
    key: opt,
    selected: value === opt,
    onClick: () => handleOption(opt)
  }, value === opt ? /*#__PURE__*/React.createElement("i", {
    className: "ri-check-line",
    "aria-hidden": "true"
  }) : null, opt))), /*#__PURE__*/React.createElement("div", {
    className: "sdc-question__custom"
  }, /*#__PURE__*/React.createElement("label", {
    className: "sdc-question__custom-label",
    htmlFor: `custom-${q.id}`
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-edit-line",
    "aria-hidden": "true"
  }), "Autre r\xE9ponse"), /*#__PURE__*/React.createElement("textarea", {
    id: `custom-${q.id}`,
    className: `sdc-question__custom-input${isCustomActive ? ' sdc-question__custom-input--active' : ''}`,
    placeholder: "Saisissez votre r\xE9ponse si aucune option ci-dessus ne convient\u2026",
    value: custom,
    onChange: handleCustomChange,
    rows: 2
  })));
}
function StepQuestions({
  questions,
  answers,
  onAnswer,
  onBack,
  onNext
}) {
  const answered = Object.keys(answers).length;
  const allDone = answered === questions.length;
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-step"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-step__intro"
  }, /*#__PURE__*/React.createElement("img", {
    className: "sdc-step__pic",
    src: "../../assets/pictograms/document-search.svg",
    alt: "",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    className: "sdc-h1"
  }, "Le mod\xE8le a ", questions.length, " questions"), /*#__PURE__*/React.createElement("p", {
    className: "sdc-lead"
  }, "Ces points d'ambigu\xEFt\xE9 changeraient la valeur d'au moins un champ du tableau final. R\xE9pondez pour lever l'incertitude \u2014 chaque r\xE9ponse est appliqu\xE9e en phase\xA02."))), /*#__PURE__*/React.createElement(QDS.Alert, {
    type: "info",
    small: true,
    title: `${answered} réponse(s) sur ${questions.length} — répondez à toutes pour continuer.`
  }), /*#__PURE__*/React.createElement("div", {
    className: "sdc-questions"
  }, questions.map(q => /*#__PURE__*/React.createElement(QuestionCard, {
    key: q.id,
    q: q,
    value: answers[q.id],
    onAnswer: onAnswer
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sdc-actions sdc-actions--split"
  }, /*#__PURE__*/React.createElement(QDS.Button, {
    variant: "secondary",
    icon: "ri-arrow-left-line",
    onClick: onBack
  }, "Retour"), /*#__PURE__*/React.createElement(QDS.Button, {
    icon: "ri-arrow-right-line",
    iconRight: true,
    disabled: !allDone,
    onClick: onNext
  }, "Produire le tableau")));
}
window.StepQuestions = StepQuestions;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/StepQuestions.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/StepVerification.jsx
try { (() => {
/* Étape 3 — Vérification : aperçu Markdown sérialisé + tableau validé contre le schéma. */
const VDS = window.SDCMetadataDesignSystem_967a78;
const VCOLUMNS = [{
  key: "table_name",
  label: "table_name",
  mono: true,
  width: "8rem"
}, {
  key: "field",
  label: "field",
  mono: true
}, {
  key: "hrc_field",
  label: "hrc_field",
  mono: true,
  width: "7rem"
}, {
  key: "indicator",
  label: "indicator",
  mono: true
}, {
  key: "hrc_indicator",
  label: "hrc_indicator",
  mono: true,
  width: "9rem"
}, {
  key: "spanning",
  label: "spanning_variables",
  mono: true
}];
function StepVerification({
  markdown,
  records,
  onBack,
  onNext
}) {
  return /*#__PURE__*/React.createElement("div", {
    className: "sdc-step"
  }, /*#__PURE__*/React.createElement("div", {
    className: "sdc-step__intro"
  }, /*#__PURE__*/React.createElement("img", {
    className: "sdc-step__pic",
    src: "../../assets/pictograms/data-visualization.svg",
    alt: "",
    "aria-hidden": "true"
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", {
    className: "sdc-h1"
  }, "V\xE9rifiez les tableaux extraits"), /*#__PURE__*/React.createElement("p", {
    className: "sdc-lead"
  }, "\xC0 gauche, le Markdown exact transmis au mod\xE8le. \xC0 droite, le tableau normalis\xE9 \u2014 une ligne par tableau statistique, valid\xE9 contre le sch\xE9ma."))), /*#__PURE__*/React.createElement("div", {
    className: "sdc-verif"
  }, /*#__PURE__*/React.createElement("section", {
    className: "sdc-verif__panel"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "sdc-panel-title"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-markdown-line",
    "aria-hidden": "true"
  }), "M\xE9tadonn\xE9es s\xE9rialis\xE9es"), /*#__PURE__*/React.createElement("pre", {
    className: "sdc-md"
  }, markdown)), /*#__PURE__*/React.createElement("section", {
    className: "sdc-verif__panel"
  }, /*#__PURE__*/React.createElement("h2", {
    className: "sdc-panel-title"
  }, /*#__PURE__*/React.createElement("i", {
    className: "ri-table-line",
    "aria-hidden": "true"
  }), "Tableau normalis\xE9"), /*#__PURE__*/React.createElement(VDS.Alert, {
    type: "success",
    small: true,
    title: `Validé contre le schéma — ${records.length} lignes, aucune erreur.`
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: "1rem"
    }
  }, /*#__PURE__*/React.createElement(VDS.Table, {
    columns: VCOLUMNS,
    rows: records,
    striped: true,
    caption: "\xAB NA \xBB = attribut sans hi\xE9rarchie. spanning_variables \u2265 1 entr\xE9e."
  })), /*#__PURE__*/React.createElement(VDS.Alert, {
    type: "warning",
    small: true,
    title: "2 hi\xE9rarchies inf\xE9r\xE9es (hrc_salades) \xE0 partir d'une note \u2014 \xE0 confirmer avant publication."
  }))), /*#__PURE__*/React.createElement("div", {
    className: "sdc-actions sdc-actions--split"
  }, /*#__PURE__*/React.createElement(VDS.Button, {
    variant: "secondary",
    icon: "ri-arrow-left-line",
    onClick: onBack
  }, "Retour aux questions"), /*#__PURE__*/React.createElement(VDS.Button, {
    icon: "ri-check-line",
    onClick: onNext
  }, "Valider et exporter")));
}
window.StepVerification = StepVerification;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/StepVerification.jsx", error: String((e && e.message) || e) }); }

// ui_kits/sdc-pipeline/data.js
try { (() => {
/* Fake data for the SDC pipeline UI kit. Mirrors the real product domain:
   a metadata workbook → serialized Markdown → questions → validated JSON table. */
(function () {
  // Serialized Markdown the model would receive (what the producer previews)
  const SAMPLE_MARKDOWN = `## Feuille « Demande_CA »  (feuille de demande)

| N° tableau | Champ              | Indicateur   | Activité (NAF) | Taille |
|------------|--------------------|--------------|----------------|--------|
| T1         | entreprises FR     | ca_total     | A88            | TREFF  |
| T2         | entreprises FR     | ca_salades   | niveau division| —      |
| T3         | entreprises FR     | ca_batavia   | niveau division| —      |

> Note : ca_salades et ca_batavia sont deux types de chiffre d'affaires « salades ».
> Tous les tableaux portent sur les entreprises françaises.

## Feuille « Nomenclature_TREFF »  (feuille de référence)

| Code | Libellé             |
|------|---------------------|
| 0    | 0 salarié           |
| 1    | 1 à 9 salariés      |
| 2    | 10 à 49 salariés    |
| 3    | 50 salariés et plus |`;

  // Phase 1 questions the model asks the producer
  const QUESTIONS = [{
    id: 1,
    category: "Indicateurs et hiérarchies",
    text: "Pour T2 et T3, « ca_batavia » est-il un composant de « ca_salades », ou une variable indépendante ?",
    ref: "Feuille Demande_CA · note ligne 5",
    options: ["Composant de ca_salades", "Variable indépendante"]
  }, {
    id: 2,
    category: "Variables de croisement et nomenclatures",
    text: "La colonne « Taille » de T1 (TREFF) renvoie-t-elle à la nomenclature « Nomenclature_TREFF » fournie dans le classeur ?",
    ref: "Feuille Demande_CA · colonne Taille",
    options: ["Oui, la nomenclature fournie", "Non, variable non structurée"]
  }, {
    id: 3,
    category: "Champ et population",
    text: "Le champ « entreprises françaises » s'applique-t-il bien aux trois tableaux, y compris ceux dont la cellule Champ est vide ?",
    ref: "Feuille Demande_CA · note finale",
    options: ["Oui, à tous les tableaux", "Non, préciser par tableau"]
  }];

  // Phase 2 — validated records (the deliverable)
  const RECORDS = [{
    table_name: "T1",
    field: "entreprises_francaises",
    hrc_field: "NA",
    indicator: "ca_total",
    hrc_indicator: "NA",
    spanning: "A88 · TREFF"
  }, {
    table_name: "T2",
    field: "entreprises_francaises",
    hrc_field: "NA",
    indicator: "ca_salades",
    hrc_indicator: "hrc_salades",
    spanning: "naf_code"
  }, {
    table_name: "T3",
    field: "entreprises_francaises",
    hrc_field: "NA",
    indicator: "ca_batavia",
    hrc_indicator: "hrc_salades",
    spanning: "naf_code"
  }];
  window.SDC_DATA = {
    SAMPLE_MARKDOWN,
    QUESTIONS,
    RECORDS
  };
})();
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/sdc-pipeline/data.js", error: String((e && e.message) || e) }); }

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Card = __ds_scope.Card;

__ds_ns.Stepper = __ds_scope.Stepper;

__ds_ns.Table = __ds_scope.Table;

__ds_ns.Alert = __ds_scope.Alert;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Tag = __ds_scope.Tag;

__ds_ns.FileUpload = __ds_scope.FileUpload;

__ds_ns.Input = __ds_scope.Input;

})();
