import type { ComponentProps } from "react";

type Props = ComponentProps<"input"> & { erro?: boolean };

const BASE =
  "h-12 w-full rounded-lg border bg-input p-4 text-small text-text placeholder:text-muted focus:outline-none focus:ring-1 " +
  "disabled:cursor-not-allowed disabled:border-line disabled:bg-line";

export function Campo({ erro = false, className = "", ...props }: Props) {
  const estado = erro ? "border-error focus:ring-error" : "border-line focus:border-brand focus:ring-brand";
  return <input aria-invalid={erro || undefined} className={`${BASE} ${estado} ${className}`} {...props} />;
}
