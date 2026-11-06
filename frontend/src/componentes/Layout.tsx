import { NavLink, Outlet } from "react-router";

// Estrutura mínima, sem estilo: implementar o layout e o design system do Figma é tarefa da equipe.
export const MENU = [
  { caminho: "/", rotulo: "Visão geral" },
  { caminho: "/trilha", rotulo: "Minha trilha" },
  { caminho: "/assistente", rotulo: "Assistente IA" },
  { caminho: "/conquistas", rotulo: "Conquistas" },
  { caminho: "/ajuda", rotulo: "Central de ajuda" },
];

export function Layout() {
  return (
    <>
      <nav aria-label="Menu principal">
        <ul>
          {MENU.map((item) => (
            <li key={item.caminho}>
              <NavLink to={item.caminho} end>
                {item.rotulo}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <main>
        <Outlet />
      </main>
    </>
  );
}
