type Props = { titulo: string; tela: string };

// Página provisória: mostra qual tela do Figma ainda falta implementar.
export function EmConstrucao({ titulo, tela }: Props) {
  return (
    <section>
      <h1>{titulo}</h1>
      <p>Em construção. Referência no Figma: tela {tela}.</p>
    </section>
  );
}
