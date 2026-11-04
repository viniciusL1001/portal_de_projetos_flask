DROP SCHEMA IF EXISTS `portal_de_projetos`;

CREATE SCHEMA IF NOT EXISTS `portal_de_projetos` DEFAULT CHARACTER SET utf8mb4;
USE `portal_de_projetos`;

DROP TABLE IF EXISTS `Usuario`;
DROP TABLE IF EXISTS `Projeto`;
DROP TABLE IF EXISTS `Comentario`;

CREATE TABLE IF NOT EXISTS `Usuario`(
    `idUsuario` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `nomeUsuario` VARCHAR(100) NOT NULL,
    `email` VARCHAR(255) NOT NULL,
    `senha` VARCHAR(255) NOT NULL,

    PRIMARY KEY(`idUsuario`),
    UNIQUE INDEX `nomeUsuario_UNIQUE` (`nomeUsuario` ASC),
    UNIQUE INDEX `email_UNIQUE` (`email` ASC)
) ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `Projeto`(
    `idProjeto` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `idUsuario` INT UNSIGNED NOT NULL,
    `titulo` VARCHAR(100) NOT NULL,
    `descricao` TEXT NULL,
    `dataCriacao` DATE NOT NULL,
    `imagem` VARCHAR(255) NULL, 
    `linkGitHub` VARCHAR(255) NOT NULL,

    PRIMARY KEY(`idProjeto`),
    INDEX `fk_Projeto_Usuario_idx` (`idUsuario`),
    FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `Comentario`(
    `idComentario` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    `idProjeto` INT UNSIGNED NOT NULL,
    `idUsuario` INT UNSIGNED NOT NULL,
    `nota` INT NULL,
    `texto` VARCHAR(1000) NOT NULL,
    `dataComentario` DATE NOT NULL,

    PRIMARY KEY(`idComentario`),
    INDEX `fk_Comentario_Projeto_idx` (`idProjeto`),
    FOREIGN KEY (`idProjeto`) REFERENCES `Projeto` (`idProjeto`) ON DELETE CASCADE,
    INDEX `fk_Comentario_Usuario_idx` (`idUsuario`),
    FOREIGN KEY (`idUsuario`) REFERENCES `Usuario` (`idUsuario`),

    CHECK(`nota` BETWEEN 1 AND 5)
) ENGINE = InnoDB;