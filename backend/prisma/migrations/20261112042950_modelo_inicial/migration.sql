-- CreateEnum
CREATE TYPE "Perfil" AS ENUM ('COLABORADOR', 'GESTOR', 'ADMIN');

-- CreateEnum
CREATE TYPE "OrigemDocumento" AS ENUM ('AUTORIZADO', 'SINTETICO', 'ANONIMIZADO');

-- CreateEnum
CREATE TYPE "StatusDocumento" AS ENUM ('PENDENTE', 'INDEXADO', 'ERRO');

-- CreateEnum
CREATE TYPE "StatusTrilha" AS ENUM ('RASCUNHO', 'EM_REVISAO', 'PUBLICADA', 'ARQUIVADA');

-- CreateEnum
CREATE TYPE "TipoAtividade" AS ENUM ('LEITURA', 'QUIZ', 'REFLEXAO');

-- CreateTable
CREATE TABLE "Usuario" (
    "id" UUID NOT NULL,
    "nome" VARCHAR(150) NOT NULL,
    "email" VARCHAR(254) NOT NULL,
    "senhaHash" TEXT NOT NULL,
    "perfil" "Perfil" NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT true,
    "criadoEm" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Usuario_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Documento" (
    "id" TEXT NOT NULL,
    "titulo" VARCHAR(255) NOT NULL,
    "descricao" TEXT,
    "origem" "OrigemDocumento" NOT NULL,
    "status" "StatusDocumento" NOT NULL,
    "ativo" BOOLEAN NOT NULL DEFAULT true,
    "criadoPorId" UUID NOT NULL,
    "criadoEm" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Documento_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Trilha" (
    "id" UUID NOT NULL,
    "titulo" VARCHAR(255) NOT NULL,
    "objetivo" TEXT NOT NULL,
    "status" "StatusTrilha" NOT NULL DEFAULT 'RASCUNHO',
    "criadoPorId" UUID NOT NULL,
    "validadaPorId" UUID,
    "validadaEm" TIMESTAMPTZ,

    CONSTRAINT "Trilha_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Milestone" (
    "id" UUID NOT NULL,
    "trilhaId" UUID NOT NULL,
    "titulo" VARCHAR(255) NOT NULL,
    "ordem" INTEGER NOT NULL,

    CONSTRAINT "Milestone_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Atividade" (
    "id" UUID NOT NULL,
    "milestoneId" UUID NOT NULL,
    "tipo" "TipoAtividade" NOT NULL,
    "descricao" TEXT NOT NULL,
    "ordem" INTEGER NOT NULL,
    "xp" INTEGER NOT NULL,
    "fontes" JSONB NOT NULL DEFAULT '[]',

    CONSTRAINT "Atividade_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Inscricao" (
    "usuarioId" UUID NOT NULL,
    "trilhaId" UUID NOT NULL,
    "iniciadaEm" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "concluidaEm" TIMESTAMPTZ,
    "abandonadaEm" TIMESTAMPTZ,

    CONSTRAINT "Inscricao_pkey" PRIMARY KEY ("usuarioId","trilhaId")
);

-- CreateTable
CREATE TABLE "AtividadeConcluida" (
    "usuarioId" UUID NOT NULL,
    "atividadeId" UUID NOT NULL,
    "concluidaEm" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "xpGanho" INTEGER NOT NULL,

    CONSTRAINT "AtividadeConcluida_pkey" PRIMARY KEY ("usuarioId","atividadeId")
);

-- CreateTable
CREATE TABLE "Tentativa" (
    "id" UUID NOT NULL,
    "usuarioId" UUID NOT NULL,
    "atividadeId" UUID NOT NULL,
    "realizadaEm" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "nota" DECIMAL(4,2),
    "respostas" JSONB,

    CONSTRAINT "Tentativa_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Usuario_email_key" ON "Usuario"("email");

-- CreateIndex
CREATE UNIQUE INDEX "Milestone_trilhaId_ordem_key" ON "Milestone"("trilhaId", "ordem");

-- CreateIndex
CREATE UNIQUE INDEX "Atividade_milestoneId_ordem_key" ON "Atividade"("milestoneId", "ordem");

-- AddForeignKey
ALTER TABLE "Documento" ADD CONSTRAINT "Documento_criadoPorId_fkey" FOREIGN KEY ("criadoPorId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Trilha" ADD CONSTRAINT "Trilha_criadoPorId_fkey" FOREIGN KEY ("criadoPorId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Trilha" ADD CONSTRAINT "Trilha_validadaPorId_fkey" FOREIGN KEY ("validadaPorId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Milestone" ADD CONSTRAINT "Milestone_trilhaId_fkey" FOREIGN KEY ("trilhaId") REFERENCES "Trilha"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Atividade" ADD CONSTRAINT "Atividade_milestoneId_fkey" FOREIGN KEY ("milestoneId") REFERENCES "Milestone"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Inscricao" ADD CONSTRAINT "Inscricao_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Inscricao" ADD CONSTRAINT "Inscricao_trilhaId_fkey" FOREIGN KEY ("trilhaId") REFERENCES "Trilha"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AtividadeConcluida" ADD CONSTRAINT "AtividadeConcluida_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AtividadeConcluida" ADD CONSTRAINT "AtividadeConcluida_atividadeId_fkey" FOREIGN KEY ("atividadeId") REFERENCES "Atividade"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Tentativa" ADD CONSTRAINT "Tentativa_usuarioId_fkey" FOREIGN KEY ("usuarioId") REFERENCES "Usuario"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Tentativa" ADD CONSTRAINT "Tentativa_atividadeId_fkey" FOREIGN KEY ("atividadeId") REFERENCES "Atividade"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddCheck
ALTER TABLE "Inscricao" ADD CONSTRAINT "Inscricao_conclusao_abandono_check"
  CHECK ("concluidaEm" IS NULL OR "abandonadaEm" IS NULL);
ALTER TABLE "Inscricao" ADD CONSTRAINT "Inscricao_concluidaEm_check"
  CHECK ("concluidaEm" IS NULL OR "concluidaEm" >= "iniciadaEm");
ALTER TABLE "Inscricao" ADD CONSTRAINT "Inscricao_abandonadaEm_check"
  CHECK ("abandonadaEm" IS NULL OR "abandonadaEm" >= "iniciadaEm");

ALTER TABLE "Milestone" ADD CONSTRAINT "Milestone_ordem_check"
  CHECK ("ordem" > 0);

ALTER TABLE "Atividade" ADD CONSTRAINT "Atividade_ordem_check"
  CHECK ("ordem" > 0);
ALTER TABLE "Atividade" ADD CONSTRAINT "Atividade_xp_check"
  CHECK ("xp" >= 0);
ALTER TABLE "Atividade" ADD CONSTRAINT "Atividade_fontes_check"
  CHECK (jsonb_typeof("fontes") = 'array');

ALTER TABLE "AtividadeConcluida" ADD CONSTRAINT "AtividadeConcluida_xpGanho_check"
  CHECK ("xpGanho" >= 0);

ALTER TABLE "Tentativa" ADD CONSTRAINT "Tentativa_nota_check"
  CHECK ("nota" BETWEEN 0 AND 10);

ALTER TABLE "Trilha" ADD CONSTRAINT "Trilha_validacao_check"
  CHECK (("validadaPorId" IS NULL) = ("validadaEm" IS NULL));