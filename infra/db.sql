CREATE TABLE public.conversions (
  id UUID STORAGE PLAIN DEFAULT gen_random_uuid() NOT NULL,
  created_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN,
  deleted_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN,
  status VARCHAR(20) DEFAULT 'Created'::character varying,
  CONSTRAINT conversions_pkey PRIMARY KEY(id)
) ;

ALTER TABLE public.conversions
  ALTER COLUMN id SET STATISTICS 0;

COMMENT ON COLUMN public.conversions.status
IS 'Created / Running / Finished / Error';


CREATE TABLE public.releases (
  id UUID STORAGE PLAIN DEFAULT gen_random_uuid() NOT NULL,
  created_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN DEFAULT CURRENT_TIMESTAMP NOT NULL,
  updated_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN,
  conversions_id UUID STORAGE PLAIN NOT NULL,
  index INTEGER STORAGE PLAIN NOT NULL,
  cd JSON NOT NULL,
  complement VARCHAR(15),
  dates JSON NOT NULL,
  descriptions JSON NOT NULL,
  documents JSON,
  parcel TEXT,
  supplier TEXT,
  identification_supplier VARCHAR(18),
  bank TEXT,
  branch TEXT,
  type TEXT,
  series TEXT,
  additional_information TEXT,
  additional_information_add TEXT,
  "values" JSON NOT NULL,
  increase NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  interest NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  fine NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  discount NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  return NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  expense NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  other NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  rebate NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  bonus NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  iof NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  mora NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  insurance NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  rate NUMERIC(12,2) STORAGE MAIN DEFAULT 0,
  debit_account TEXT,
  credit_account TEXT,
  reduced_account TEXT,
  full_account TEXT,
  account_description TEXT,
  balancing_entry TEXT,
  CONSTRAINT releases_pkey PRIMARY KEY(id),
  CONSTRAINT releases_fk_conversions FOREIGN KEY (conversions_id)
    REFERENCES public.conversions(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    NOT DEFERRABLE
) ;

ALTER TABLE public.releases
  ALTER COLUMN id SET STATISTICS 0;

COMMENT ON COLUMN public.releases.parcel
IS 'Parcela';

COMMENT ON COLUMN public.releases.supplier
IS 'Fornecedor';

COMMENT ON COLUMN public.releases.identification_supplier
IS 'CPF/CNPJ Fornecedor';

COMMENT ON COLUMN public.releases.bank
IS 'Banco';

COMMENT ON COLUMN public.releases.branch
IS 'Filial';

COMMENT ON COLUMN public.releases.type
IS 'Espécie';

COMMENT ON COLUMN public.releases.series
IS 'Série';

COMMENT ON COLUMN public.releases.additional_information
IS 'Informação Adicional';

COMMENT ON COLUMN public.releases.additional_information_add
IS 'Informação Adicional 3';

COMMENT ON COLUMN public.releases.increase
IS 'Acréscimo';

COMMENT ON COLUMN public.releases.interest
IS 'Juros';

COMMENT ON COLUMN public.releases.fine
IS 'Multa';

COMMENT ON COLUMN public.releases.discount
IS 'Desconto';

COMMENT ON COLUMN public.releases.return
IS 'Devolução';

COMMENT ON COLUMN public.releases.expense
IS 'Despesa';

COMMENT ON COLUMN public.releases.other
IS 'Outros';

COMMENT ON COLUMN public.releases.rebate
IS 'Abatimento';

COMMENT ON COLUMN public.releases.bonus
IS 'Bonificação';

COMMENT ON COLUMN public.releases.iof
IS 'IOF';

COMMENT ON COLUMN public.releases.mora
IS 'Mora';

COMMENT ON COLUMN public.releases.insurance
IS 'Seguro';

COMMENT ON COLUMN public.releases.rate
IS 'Tarifa';

COMMENT ON COLUMN public.releases.debit_account
IS 'Conta débito';

COMMENT ON COLUMN public.releases.credit_account
IS 'Conta crédito';

COMMENT ON COLUMN public.releases.reduced_account
IS 'Conta reduzida';

COMMENT ON COLUMN public.releases.full_account
IS 'Conta completa';

COMMENT ON COLUMN public.releases.account_description
IS 'Conta descrição';

COMMENT ON COLUMN public.releases.balancing_entry
IS 'Conta partida';

CREATE UNIQUE INDEX releases_idx_conversions ON public.releases
  USING btree (conversions_id, index);


CREATE TABLE public.files (
  id UUID STORAGE PLAIN DEFAULT gen_random_uuid() NOT NULL,
  created_at TIMESTAMP(0) WITHOUT TIME ZONE STORAGE PLAIN DEFAULT CURRENT_TIMESTAMP NOT NULL,
  conversions_id UUID STORAGE PLAIN NOT NULL,
  name VARCHAR(255),
  mime VARCHAR(100) NOT NULL,
  base64 TEXT,
  status VARCHAR(100),
  error TEXT,
  CONSTRAINT files_pkey PRIMARY KEY(id),
  CONSTRAINT files_fk_conversions FOREIGN KEY (conversions_id)
    REFERENCES public.conversions(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
    NOT DEFERRABLE
) ;

ALTER TABLE public.files
  ALTER COLUMN id SET STATISTICS 0;

CREATE ROLE anon NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT LOGIN NOREPLICATION NOBYPASSRLS;
GRANT ALL ON SCHEMA public TO anon;
GRANT ALL ON TABLE public.conversions TO anon;
GRANT ALL ON TABLE public.files TO anon;
GRANT ALL ON TABLE public.releases TO anon;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO anon;

