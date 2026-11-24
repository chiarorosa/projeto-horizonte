type Props = { titulo: string; tela: string };

// Página provisória: mostra qual tela do Figma ainda falta implementar.
export function EmConstrucao({ titulo, tela }: Props) {
  return (
    <section className="flex flex-col gap-2">
      <h1 className="text-h1 text-text">{titulo}</h1>
      <p className="text-body text-muted">Em construção. Referência no Figma: tela {tela}.</p>
    </section>
  );
}
