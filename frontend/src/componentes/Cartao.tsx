import type { ComponentProps } from "react";

export function Cartao({ className = "", ...props }: ComponentProps<"div">) {
  return <div className={`rounded-2xl bg-panel p-6 shadow-painel ${className}`} {...props} />;
}
