# Carnaval de Barranquilla

La plataforma definitiva para descubrir todo sobre el **Carnaval de Barranquilla** — Patrimonio Oral e Inmaterial de la Humanidad.

Un hub centralizado que reúne noticias, eventos, servicios, productos, planes turísticos y todo lo que gira alrededor de la fiesta más grande de Colombia.

## Estructura del Proyecto

```
carnaval-de-barranquilla/
├── scrapers/          # Python - Motor de scraping y recolección de datos
├── web/               # Next.js - Frontend + API
├── supabase/          # Schema y migraciones de base de datos
└── .github/           # CI/CD workflows
```

## Tech Stack

| Capa | Tecnología |
|------|-----------|
| Scraping | Python, Scrapy, BeautifulSoup, Playwright |
| Frontend | Next.js 14, TypeScript, Tailwind CSS |
| Base de datos | Supabase (PostgreSQL) |
| Deploy | TBD |

## Categorías de Datos

- **Noticias** — Artículos y cobertura de medios locales y nacionales
- **Eventos** — Desfiles, comparsas, fiestas, conciertos, agenda completa
- **Servicios** — Hoteles, restaurantes, transporte, guías turísticos
- **Productos** — Merchandising, artesanías, disfraces, accesorios
- **Planes** — Paquetes turísticos, experiencias, rutas recomendadas

## Desarrollo

### Scrapers (Python)

```bash
cd scrapers
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
scrapy crawl news
```

### Web (Next.js)

```bash
cd web
npm install
npm run dev
```

## Fases del Proyecto

1. **Fundación** — Repo, estructura, DB schema, primer scraper
2. **Motor de Scraping** — Scrapers para todas las fuentes de datos
3. **API y Datos** — Endpoints, búsqueda, categorización
4. **Landing Page** — UX de primera clase para explorar el Carnaval
5. **Features Avanzados** — Cuentas, favoritos, mapa interactivo
6. **Lanzamiento** — SEO, analytics, partnerships

## Licencia

MIT
