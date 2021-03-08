create table Paciente (
	cod_paciente integer PRIMARY KEY,
	nome varchar(100),
	sexo varchar(1)
);

create table pedido
(
	cod_pedido  varchar(70),
	ordem_servico integer PRIMARY KEY,
	cod_paciente integer NOT NULL,
    FOREIGN KEY (cod_paciente) REFERENCES paciente(cod_paciente)
);

create table exame
(
	cod_exame integer PRIMARY KEY,
	descricao varchar(100)
);

create table pedido_exame
(
	ordem_servico integer not null,
	cod_exame  integer not null,
	FOREIGN KEY (ordem_servico) REFERENCES pedido(ordem_servico),
	FOREIGN KEY (cod_exame) REFERENCES exame(cod_exame)

)

insert into exame values (100, 'Hemograma');
insert into exame values (101, 'Gligose');
insert into exame values (102, 'T4');
insert into exame values (103, 'TSH');