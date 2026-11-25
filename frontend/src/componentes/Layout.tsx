import { Link, NavLink, Outlet, useLocation } from "react-router";
import award from "../assets/icones/award.svg";
import bell from "../assets/icones/bell.svg";
import book from "../assets/icones/book.svg";
import chat from "../assets/icones/chat.svg";
import help from "../assets/icones/help.svg";
import home from "../assets/icones/home.svg";
import marca from "../assets/icones/marca.svg";
import search from "../assets/icones/search.svg";
import shield from "../assets/icones/shield.svg";

export const MENU = [
  { caminho: "/", rotulo: "Visão geral", icone: home },
  { caminho: "/trilha", rotulo: "Minha trilha", icone: book },
  { caminho: "/assistente", rotulo: "Assistente IA", icone: chat },
  { caminho: "/conquistas", rotulo: "Conquistas", icone: award },
  { caminho: "/ajuda", rotulo: "Central de ajuda", icone: help },
];

// Ícones do Figma (cinza). No item ativo o filtro deixa o mesmo ícone branco.
function Icone({ src, className = "size-5", branco = false }: { src: string; className?: string; branco?: boolean }) {
  return <img src={src} alt="" className={`${className} shrink-0 ${branco ? "brightness-0 invert" : ""}`} />;
}

function MenuLateral() {
  return (
    <aside className="sticky top-0 flex h-screen w-60 shrink-0 flex-col gap-8 border-r border-line bg-panel p-6">
      <Link to="/" className="flex items-center gap-3">
        <img src={marca} alt="" className="size-8" />
        <span className="text-h3 text-text">Onboarding</span>
      </Link>
      <p className="text-small text-muted">Espaço do colaborador</p>

      <nav aria-label="Menu principal">
        <ul className="flex flex-col gap-2">
          {MENU.map((item) => (
            <li key={item.caminho}>
              <NavLink
                to={item.caminho}
                end
                className={({ isActive }) =>
                  `flex h-12 items-center gap-3 rounded-lg p-3 text-label ${
                    isActive ? "bg-brand text-white" : "text-muted hover:bg-canvas"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icone src={item.icone} branco={isActive} />
                    {item.rotulo}
                  </>
                )}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="mt-auto flex flex-col gap-5">
        {/* Visual por enquanto: o aviso de privacidade é uma tela própria. */}
        <button type="button" className="flex items-start gap-2 text-small text-muted">
          <Icone src={shield} className="size-4" />
          Privacidade
        </button>
        <div className="h-px bg-inverse opacity-15" />
        {/* Usuário de exemplo do Figma; virá da autenticação quando ela existir. */}
        <div className="flex items-center gap-3">
          <span className="flex size-9 shrink-0 items-center justify-center rounded-full bg-brand text-label text-white">
            LS
          </span>
          <div className="flex flex-col gap-1 text-muted">
            <span className="text-label">Lucas Silva</span>
            <span className="text-xs">Administrativo</span>
          </div>
        </div>
      </div>
    </aside>
  );
}

function BarraSuperior() {
  const { pathname } = useLocation();
  const titulo = MENU.find((item) => item.caminho === pathname)?.rotulo ?? "";

  return (
    <header className="flex h-19 shrink-0 items-center justify-between gap-6 border-b border-line bg-panel px-10">
      <p className="text-label text-muted">{titulo}</p>
      {/* Busca e notificações são só visuais (fora do escopo da Issue #45). */}
      <div
        aria-hidden="true"
        className="flex h-11 w-120 items-center gap-3 rounded-[10px] border border-line bg-input px-4 py-2.5 text-small text-muted"
      >
        <Icone src={search} />
        Buscar conteúdos e atividades
      </div>
      <div className="flex items-center gap-5">
        <button type="button" aria-label="Notificações" className="flex h-11 w-10 items-center justify-center text-muted">
          <Icone src={bell} />
        </button>
        <span className="flex size-9 items-center justify-center rounded-full bg-brandSoft text-label text-brand">LS</span>
      </div>
    </header>
  );
}

export function Layout() {
  return (
    <div className="flex min-h-screen bg-canvas">
      <MenuLateral />
      <div className="flex min-w-0 flex-1 flex-col">
        <BarraSuperior />
        <main className="px-10 pt-8 pb-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
