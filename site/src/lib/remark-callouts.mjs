import { visit } from "unist-util-visit";

// :::warning / :::do / :::note / :::emergency / :::stats container directives.
// Any other directive syntax (e.g. "insuline:glucides" parsed as a text
// directive) is turned back into the literal text it came from.
const KINDS = new Set(["warning", "do", "note", "emergency", "stats"]);

function literal(node) {
  const text = node.children?.map((c) => c.value ?? "").join("") ?? "";
  const prefix = node.type === "textDirective" ? ":" : node.type === "leafDirective" ? "::" : ":::";
  return prefix + node.name + (text ? `[${text}]` : "");
}

export function remarkCallouts() {
  return (tree) => {
    visit(tree, (node, index, parent) => {
      if (!["containerDirective", "leafDirective", "textDirective"].includes(node.type)) return;
      if (node.type === "containerDirective" && KINDS.has(node.name)) {
        const first = node.children[0];
        if (first?.data?.directiveLabel) {
          first.data = { hName: "p", hProperties: { className: ["callout-title"] } };
        }
        node.data = {
          hName: node.name === "stats" ? "div" : "aside",
          hProperties: { className: ["callout", `callout-${node.name}`] },
        };
        return;
      }
      if (parent && index != null) {
        parent.children.splice(index, 1, { type: "text", value: literal(node) });
      }
    });
  };
}
