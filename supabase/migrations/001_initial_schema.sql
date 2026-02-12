-- =============================================
-- Carnaval de Barranquilla - Database Schema
-- =============================================
-- Supabase (PostgreSQL) schema for storing all
-- scraped data about the Carnaval.
-- =============================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For fuzzy text search

-- =============================================
-- SOURCES: Fuentes de datos (sitios web, redes)
-- =============================================
CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL CHECK (type IN ('news', 'social', 'business_directory', 'event_portal', 'marketplace', 'government', 'other')),
    is_active BOOLEAN DEFAULT true,
    scrape_frequency_hours INTEGER DEFAULT 24,
    last_scraped_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- CATEGORIES: Categorías y tags
-- =============================================
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_id UUID REFERENCES categories(id),
    icon TEXT,
    color TEXT,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- =============================================
-- ARTICLES: Noticias y artículos
-- =============================================
CREATE TABLE articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    title TEXT NOT NULL,
    url TEXT NOT NULL UNIQUE,
    author TEXT,
    published_at TIMESTAMPTZ,
    summary TEXT,
    content TEXT,
    image_url TEXT,
    tags TEXT[],
    category_id UUID REFERENCES categories(id),
    is_featured BOOLEAN DEFAULT false,
    view_count INTEGER DEFAULT 0,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Full-text search index for articles
CREATE INDEX idx_articles_fts ON articles
    USING GIN (to_tsvector('spanish', coalesce(title, '') || ' ' || coalesce(summary, '') || ' ' || coalesce(content, '')));

CREATE INDEX idx_articles_published ON articles(published_at DESC);
CREATE INDEX idx_articles_source ON articles(source_id);
CREATE INDEX idx_articles_category ON articles(category_id);

-- =============================================
-- EVENTS: Eventos del Carnaval
-- =============================================
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    description TEXT,
    event_date DATE,
    event_time TIME,
    end_date DATE,
    end_time TIME,
    location_name TEXT,
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    image_url TEXT,
    category_id UUID REFERENCES categories(id),
    price DECIMAL(12, 2),
    currency TEXT DEFAULT 'COP',
    is_free BOOLEAN DEFAULT false,
    is_featured BOOLEAN DEFAULT false,
    status TEXT DEFAULT 'upcoming' CHECK (status IN ('upcoming', 'ongoing', 'completed', 'cancelled')),
    tags TEXT[],
    extra_data JSONB,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_location ON events USING GIST (
    point(longitude, latitude)
) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX idx_events_fts ON events
    USING GIN (to_tsvector('spanish', coalesce(title, '') || ' ' || coalesce(description, '')));

-- =============================================
-- BUSINESSES: Negocios y servicios
-- =============================================
CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    name TEXT NOT NULL,
    url TEXT UNIQUE,
    description TEXT,
    category_id UUID REFERENCES categories(id),
    address TEXT,
    city TEXT DEFAULT 'Barranquilla',
    phone TEXT,
    email TEXT,
    website TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    rating DECIMAL(3, 2),
    review_count INTEGER DEFAULT 0,
    image_url TEXT,
    images TEXT[],
    opening_hours JSONB,
    price_range TEXT CHECK (price_range IN ('$', '$$', '$$$', '$$$$')),
    is_verified BOOLEAN DEFAULT false,
    is_featured BOOLEAN DEFAULT false,
    tags TEXT[],
    extra_data JSONB,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_businesses_category ON businesses(category_id);
CREATE INDEX idx_businesses_rating ON businesses(rating DESC NULLS LAST);
CREATE INDEX idx_businesses_location ON businesses USING GIST (
    point(longitude, latitude)
) WHERE latitude IS NOT NULL AND longitude IS NOT NULL;
CREATE INDEX idx_businesses_fts ON businesses
    USING GIN (to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, '')));

-- =============================================
-- PRODUCTS: Productos y merchandising
-- =============================================
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    name TEXT NOT NULL,
    url TEXT UNIQUE,
    description TEXT,
    price DECIMAL(12, 2),
    currency TEXT DEFAULT 'COP',
    image_url TEXT,
    images TEXT[],
    category_id UUID REFERENCES categories(id),
    seller TEXT,
    availability TEXT DEFAULT 'available' CHECK (availability IN ('available', 'out_of_stock', 'pre_order')),
    tags TEXT[],
    extra_data JSONB,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_fts ON products
    USING GIN (to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, '')));

-- =============================================
-- PLANS: Planes turísticos y paquetes
-- =============================================
CREATE TABLE plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    description TEXT,
    price DECIMAL(12, 2),
    currency TEXT DEFAULT 'COP',
    duration TEXT,
    includes TEXT[],
    image_url TEXT,
    images TEXT[],
    provider TEXT,
    category_id UUID REFERENCES categories(id),
    is_featured BOOLEAN DEFAULT false,
    tags TEXT[],
    extra_data JSONB,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_plans_category ON plans(category_id);
CREATE INDEX idx_plans_price ON plans(price);
CREATE INDEX idx_plans_fts ON plans
    USING GIN (to_tsvector('spanish', coalesce(title, '') || ' ' || coalesce(description, '')));

-- =============================================
-- MEDIA: Fotos y videos
-- =============================================
CREATE TABLE media (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    url TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('image', 'video', 'audio')),
    title TEXT,
    description TEXT,
    thumbnail_url TEXT,
    width INTEGER,
    height INTEGER,
    duration_seconds INTEGER,
    tags TEXT[],
    related_article_id UUID REFERENCES articles(id),
    related_event_id UUID REFERENCES events(id),
    extra_data JSONB,
    scraped_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_media_type ON media(type);

-- =============================================
-- SCRAPE_LOGS: Registro de ejecuciones
-- =============================================
CREATE TABLE scrape_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    spider_name TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
    items_scraped INTEGER DEFAULT 0,
    items_new INTEGER DEFAULT 0,
    items_updated INTEGER DEFAULT 0,
    items_dropped INTEGER DEFAULT 0,
    errors TEXT[],
    started_at TIMESTAMPTZ DEFAULT NOW(),
    finished_at TIMESTAMPTZ,
    duration_seconds INTEGER,
    extra_data JSONB
);

CREATE INDEX idx_scrape_logs_source ON scrape_logs(source_id);
CREATE INDEX idx_scrape_logs_status ON scrape_logs(status);
CREATE INDEX idx_scrape_logs_started ON scrape_logs(started_at DESC);

-- =============================================
-- SEED DATA: Categorías iniciales
-- =============================================
INSERT INTO categories (name, slug, description, sort_order) VALUES
    ('Noticias', 'noticias', 'Artículos y cobertura de medios', 1),
    ('Eventos', 'eventos', 'Desfiles, comparsas, fiestas y conciertos', 2),
    ('Servicios', 'servicios', 'Hoteles, restaurantes, transporte', 3),
    ('Productos', 'productos', 'Merchandising, artesanías, disfraces', 4),
    ('Planes', 'planes', 'Paquetes turísticos y experiencias', 5),
    ('Gastronomía', 'gastronomia', 'Comida típica y restaurantes', 6),
    ('Cultura', 'cultura', 'Historia, tradiciones y patrimonio', 7),
    ('Música', 'musica', 'Artistas, géneros y presentaciones', 8),
    ('Transporte', 'transporte', 'Cómo llegar y moverse', 9),
    ('Alojamiento', 'alojamiento', 'Hoteles, hostales y apartamentos', 10);

-- Subcategorías de eventos
INSERT INTO categories (name, slug, description, parent_id, sort_order)
SELECT name, slug, description, (SELECT id FROM categories WHERE slug = 'eventos'), sort_order
FROM (VALUES
    ('Desfiles', 'desfiles', 'La Batalla de Flores, Gran Parada y más', 1),
    ('Comparsas', 'comparsas', 'Grupos de danza y comparsas tradicionales', 2),
    ('Fiestas', 'fiestas', 'Fiestas privadas y públicas', 3),
    ('Conciertos', 'conciertos', 'Presentaciones musicales en vivo', 4),
    ('Reinados', 'reinados', 'Elecciones y concursos de belleza', 5)
) AS t(name, slug, description, sort_order);

-- Initial sources
INSERT INTO sources (name, url, type) VALUES
    ('El Heraldo', 'https://www.elheraldo.co', 'news'),
    ('El Universal', 'https://www.eluniversal.com.co', 'news'),
    ('Blu Radio', 'https://www.bluradio.com', 'news'),
    ('Carnaval de Barranquilla (Oficial)', 'https://www.carnavaldebarranquilla.org', 'event_portal'),
    ('Alcaldía de Barranquilla', 'https://www.barranquilla.gov.co', 'government');

-- =============================================
-- FUNCTIONS: Updated_at trigger
-- =============================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_updated_at BEFORE UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER events_updated_at BEFORE UPDATE ON events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER businesses_updated_at BEFORE UPDATE ON businesses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER plans_updated_at BEFORE UPDATE ON plans
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER sources_updated_at BEFORE UPDATE ON sources
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
