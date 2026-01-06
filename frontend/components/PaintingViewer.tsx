"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";

interface Painting {
  id: string;
  name: string;
  artist_name: string;
  artist_slug: string;
  painting_slug: string;
  museum_name: string | null;
  genre_name: string[] | null;
  image_url: string;
  source_url: string;
  license_name: string | null;
  license_url: string | null;
  facts_count: number;
}

interface Fact {
  id: string;
  painting_id: string;
  name: string;
  description_md: string;
  geometry_type: string;
  x: number;
  y: number;
  w: number;
  h: number;
  order_index: number;
}

interface Props {
  painting: Painting;
  facts: Fact[];
}

const slugify = (value: string) =>
  value
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[^\p{L}\p{N}]+/gu, "-")
    .replace(/^-+|-+$/g, "");

export default function PaintingViewer({ painting, facts }: Props) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const imageRef = useRef<HTMLImageElement | null>(null);
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  const { factSlugById, factIdBySlug } = useMemo(() => {
    const slugCounts = new Map<string, number>();
    const slugById = new Map<string, string>();
    const idBySlug = new Map<string, string>();

    facts.forEach((fact, index) => {
      const base = slugify(fact.name) || `fact-${index + 1}`;
      const count = slugCounts.get(base) ?? 0;
      const slug = count === 0 ? base : `${base}-${count + 1}`;
      slugCounts.set(base, count + 1);
      slugById.set(fact.id, slug);
      idBySlug.set(slug, fact.id);
    });

    return { factSlugById: slugById, factIdBySlug: idBySlug };
  }, [facts]);

  useEffect(() => {
    const current = searchParams.get("fact");
    setSelectedId(current ? factIdBySlug.get(current) ?? null : null);
  }, [factIdBySlug, searchParams]);

  useEffect(() => {
    if (!imageRef.current) {
      return;
    }
    const updateSize = () => {
      if (!imageRef.current) {
        return;
      }
      const { width, height } = imageRef.current.getBoundingClientRect();
      setImageSize({ width, height });
    };
    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(imageRef.current);
    return () => observer.disconnect();
  }, []);

  const highlightId = selectedId ? null : hoveredId;
  const selectedFact = useMemo(
    () => facts.find((fact) => fact.id === selectedId) ?? null,
    [facts, selectedId],
  );

  const handleSelect = (factId: string) => {
    setSelectedId(factId);
    setHoveredId(null);
    const params = new URLSearchParams(searchParams.toString());
    const slug = factSlugById.get(factId) ?? factId;
    params.set("fact", slug);
    router.replace(`${pathname}?${params.toString()}`, { scroll: false });
  };

  const clearSelection = () => {
    setSelectedId(null);
    const params = new URLSearchParams(searchParams.toString());
    params.delete("fact");
    const next = params.toString();
    router.replace(next ? `${pathname}?${next}` : pathname, { scroll: false });
  };

  const getHighlightRect = (fact: Fact) => {
    const factWidth = fact.w * imageSize.width;
    const factHeight = fact.h * imageSize.height;
    const lensWidth = factWidth;
    const lensHeight = factHeight;
    const centerX = (fact.x + fact.w / 2) * imageSize.width;
    const centerY = (fact.y + fact.h / 2) * imageSize.height;
    const left = fact.x * imageSize.width;
    const top = fact.y * imageSize.height;

    return {
      left,
      top,
      width: lensWidth,
      height: lensHeight,
      centerX,
      centerY,
    };
  };

  const modalImageStyle = useMemo(() => {
    if (!selectedFact || imageSize.width === 0 || imageSize.height === 0) {
      return null;
    }
    const zoom = 3;
    const lensRect = getHighlightRect(selectedFact);
    const backgroundSize = `${imageSize.width * zoom}px ${imageSize.height * zoom}px`;
    const backgroundPosition = `${-lensRect.left * zoom}px ${-lensRect.top * zoom}px`;

    return {
      width: lensRect.width * zoom,
      height: lensRect.height * zoom,
      backgroundSize,
      backgroundPosition,
    };
  }, [selectedFact, imageSize]);

  useEffect(() => {
    if (!selectedId) {
      return;
    }
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        clearSelection();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [selectedId]);

  const genresLabel = painting.genre_name?.filter(Boolean).join(", ");

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800 bg-slate-900/80">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="text-lg font-semibold">Art Explorer</div>
          <div className="flex items-center gap-4 text-sm text-slate-400">
            <span className="cursor-not-allowed">Жанры</span>
            <input
              disabled
              placeholder="Поиск"
              className="rounded-full border border-slate-700 bg-slate-800 px-3 py-1 text-xs text-slate-500"
            />
          </div>
        </div>
      </header>

      <main className="mx-auto grid max-w-6xl gap-10 px-6 py-10 lg:grid-cols-[2fr_1fr]">
        <section className="relative">
          <div
            className="relative rounded-2xl border border-slate-800 bg-slate-900 shadow-lg"
            onMouseLeave={() => setHoveredId(null)}
          >
            <div className="relative overflow-hidden rounded-2xl">
              <img
                ref={imageRef}
                src={painting.image_url}
                alt={`${painting.name} by ${painting.artist_name}`}
                className="block h-auto w-full"
              />
              {!selectedId && imageSize.width > 0 && imageSize.height > 0 && (
              <svg
                className="absolute inset-0 h-full w-full"
                viewBox={`0 0 ${imageSize.width} ${imageSize.height}`}
                preserveAspectRatio="none"
              >
                {facts.map((fact) => {
                  const lensRect = getHighlightRect(fact);
                  const isActive = highlightId === fact.id;
                  const fill = isActive ? "rgba(56,189,248,0.18)" : "rgba(56,189,248,0.08)";
                  const stroke = isActive ? "rgba(56,189,248,0.95)" : "rgba(56,189,248,0.35)";
                  const strokeWidth = isActive ? 3 : 1.5;
                  return (
                    <rect
                      key={fact.id}
                      x={lensRect.left}
                      y={lensRect.top}
                      width={lensRect.width}
                      height={lensRect.height}
                      fill={fill}
                      stroke={stroke}
                      strokeWidth={strokeWidth}
                      rx="6"
                      onMouseEnter={() => {
                        if (!selectedId) {
                          setHoveredId(fact.id);
                        }
                      }}
                      onMouseLeave={() => setHoveredId(null)}
                      onClick={() => handleSelect(fact.id)}
                      className="cursor-pointer transition"
                    />
                  );
                })}
              </svg>
            )}
            </div>
          </div>
        </section>

        <aside className="space-y-6">
          <div className="space-y-2">
            <h1 className="text-3xl font-semibold">{painting.name}</h1>
            <p className="text-slate-300">{painting.artist_name}</p>
            <div className="flex flex-wrap gap-2 text-xs text-slate-400">
              {painting.museum_name && <span>{painting.museum_name}</span>}
              {genresLabel && <span>• {genresLabel}</span>}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4">
            <div className="mb-3 flex items-center justify-between">
              <h2 className="text-lg font-semibold">Факты по деталям</h2>
              {selectedId && (
                <button
                  onClick={clearSelection}
                  className="text-xs text-slate-400 transition hover:text-slate-200"
                >
                  Снять выделение ✕
                </button>
              )}
            </div>
            <ul className="space-y-3">
              {facts.map((fact) => {
                const isHighlighted = highlightId === fact.id;
                const isSelected = selectedId === fact.id;
                const isActive = isHighlighted || isSelected;
                return (
                  <li
                    key={fact.id}
                    className={`cursor-pointer rounded-xl border px-3 py-2 transition ${
                      isActive ? "border-sky-400 bg-slate-800" : "border-slate-800"
                    }`}
                    onMouseEnter={() => setHoveredId(fact.id)}
                    onMouseLeave={() => setHoveredId(null)}
                    onClick={() => handleSelect(fact.id)}
                  >
                    <div className="text-sm font-semibold text-slate-100">{fact.name}</div>
                    {isSelected && (
                      <div className="prose prose-invert mt-2 text-sm text-slate-300">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          rehypePlugins={[rehypeSanitize]}
                          components={{
                            a: ({ node, ...props }) => (
                              <a {...props} target="_blank" rel="noreferrer" />
                            ),
                          }}
                        >
                          {fact.description_md}
                        </ReactMarkdown>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>

          <div className="rounded-2xl border border-slate-800 bg-slate-900 p-4 text-sm text-slate-300">
            <h3 className="mb-2 text-base font-semibold text-slate-100">Атрибуция</h3>
            <p>
              Автор: <span className="text-slate-100">{painting.artist_name}</span>
            </p>
            {painting.museum_name && <p>Местоположение: {painting.museum_name}</p>}
            {genresLabel && <p>Жанры: {genresLabel}</p>}
            {painting.license_name && <p>Лицензия: {painting.license_name}</p>}
          </div>
        </aside>
      </main>

      {selectedFact && modalImageStyle && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-6 py-10 backdrop-blur-sm"
          onClick={clearSelection}
        >
          <div
            className="relative flex w-full max-w-4xl flex-col gap-6 overflow-hidden rounded-3xl border border-slate-800 bg-slate-900 p-6 shadow-2xl lg:flex-row"
            onClick={(event) => event.stopPropagation()}
          >
            <div
              className="flex-shrink-0 overflow-hidden rounded-2xl border border-slate-800 bg-slate-950"
              style={{
                width: modalImageStyle.width,
                height: modalImageStyle.height,
                backgroundImage: `url(${painting.image_url})`,
                backgroundSize: modalImageStyle.backgroundSize,
                backgroundPosition: modalImageStyle.backgroundPosition,
              }}
            />
            <div className="flex-1">
              <div className="mb-3 flex items-start justify-between gap-3">
                <div>
                  <div className="text-sm uppercase tracking-wide text-slate-400">
                    Фрагмент картины
                  </div>
                  <h3 className="text-2xl font-semibold text-slate-100">{selectedFact.name}</h3>
                </div>
                <button
                  onClick={clearSelection}
                  className="flex h-8 w-8 items-center justify-center rounded-full border border-slate-700 text-slate-300 transition hover:border-slate-500 hover:text-slate-100"
                  aria-label="Закрыть"
                >
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-4 w-4"
                  >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>
              <div className="prose prose-invert text-sm text-slate-300">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeSanitize]}
                  components={{
                    a: ({ node, ...props }) => <a {...props} target="_blank" rel="noreferrer" />,
                  }}
                >
                  {selectedFact.description_md}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
