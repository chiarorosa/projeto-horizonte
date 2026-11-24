import type { ComponentProps } from "react";

type Props = ComponentProps<"button"> & { variante?: "primario" | "secundario" };

const BASE =
  "inline-flex h-11 items-center justify-center rounded-lg border p-3 text-button focus-visible:outline-none " +
  "disabled:cursor-not-allowed disabled:border-line disabled:bg-line disabled:text-muted";

const VARIANTES = {
  primario:
    "border-transparent bg-brand text-white enabled:hover:bg-brandHover " +
    "focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2",
  secundario: "border-line bg-panel text-text focus-visible:border-brand focus-visible:ring-1 focus-visible:ring-brand",
};

export function Botao({ variante = "primario", className = "", type = "button", ...props }: Props) {
  return <button type={type} className={`${BASE} ${VARIANTES[variante]} ${className}`} {...props} />;
}
