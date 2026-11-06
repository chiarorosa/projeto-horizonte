import { NavLink, Outlet, useLocation } from "react-router";

// Itens do menu lateral das telas 09 e 19 do Figma.
export const MENU = [
  { caminho: "/", rotulo: "Visão geral" },
  { caminho: "/trilha", rotulo: "Minha trilha" },
  { caminho: "/assistente", rotulo: "Assistente IA" },
  { caminho: "/conquistas", rotulo: "Conquistas" },
  { caminho: "/ajuda", rotulo: "Central de ajuda" },
];

export function Layout() {
  const { pathname } = useLocation();
  const atual = MENU.find((item) => item.caminho === pathname)?.rotulo ?? "";

  return (
    <div className="layout">
      <aside className="menu-lateral">
        <NavLink to="/" className="marca">
          Onboarding
          <small>Espaço do colaborador</small>
        </NavLink>
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
        <div className="rodape">Privacidade</div>
      </aside>
      <div>
        <header className="barra-superior">{atual}</header>
        <main className="conteudo">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
