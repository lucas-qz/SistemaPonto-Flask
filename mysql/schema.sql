CREATE DATABASE banco1; 

use banco1;

CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nome_usuario` varchar(50) NOT NULL,
  `login_usuario` varchar(20) NOT NULL,
  `senha_usuario` varchar(255) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `login_usuario` (`login_usuario`)
);

CREATE TABLE `marcacao` (
  `id_hr` int NOT NULL AUTO_INCREMENT,
  `data` datetime NOT NULL,
  `dia` varchar(50) NOT NULL,
  `mes` varchar(50) NOT NULL,
  `ano` varchar(50) NOT NULL,
  `hora` varchar(50) NOT NULL,
  `st` varchar(2) NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_hr`)
);

