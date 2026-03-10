import { useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, Rect, Textbox } from 'fabric'

type GenerateResponse = {
  mode: string
  provider: string
  slides: Array<{ index: number; text: string; asset_kind: string }>
}

type ThemeMap = Record<string, {
  palette: string
  headline: string
  body: string
  style: string
  identity?: {
    direction?: string
    inspired_by?: string
  }
}>

type LayoutMap = Record<string, {
  description: string
  identity: { mood: string; grid: string; headline_style: string; body_style: string; accent_usage: string }
  rules: { slide_range: [number, number]; first_slide: string; middle_slides: string; last_slide: string }
}>

type CapabilityResponse = {
  can_build_similar: boolean
  supported_slide_range: [number, number]
  supported_layouts: string[]
  notes: string[]
}

type ExampleResponse = {
  title: string
  template: string
  slides: string[]
  visual_recipe: {
    headline_font: string
    body_font: string
    composition: string
  }
}

const API = 'http://localhost:8000'

export function App() {
  const [niche, setNiche] = useState('Games')
  const [template, setTemplate] = useState('Provocacao Viral')
  const [layoutName, setLayoutName] = useState('Template Autoral')
  const [rawText, setRawText] = useState('Cole seu texto bruto aqui para distribuir nos slides.')
  const [slideCount, setSlideCount] = useState(8)
  const [result, setResult] = useState<GenerateResponse | null>(null)
  const [themes, setThemes] = useState<ThemeMap>({})
  const [layouts, setLayouts] = useState<LayoutMap>({})
  const [capability, setCapability] = useState<CapabilityResponse | null>(null)
  const [example, setExample] = useState<ExampleResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  const slides = result?.slides ?? []
  const activeSlide = useMemo(() => slides[0], [slides])
  const selectedTheme = themes[niche]
  const selectedLayout = layouts[layoutName]

  useEffect(() => {
    fetch(`${API}/api/themes`).then((r) => r.json()).then(setThemes).catch(() => undefined)
    fetch(`${API}/api/layouts`).then((r) => r.json()).then(setLayouts).catch(() => undefined)
    fetch(`${API}/api/capability`).then((r) => r.json()).then(setCapability).catch(() => undefined)
  }, [])

  useEffect(() => {
    if (!canvasRef.current) return
    const canvas = new Canvas(canvasRef.current, { width: 540, height: 540, backgroundColor: '#0b0b0f' })

    canvas.add(new Rect({ left: 0, top: 0, width: 540, height: 84, fill: selectedTheme?.palette ?? '#9D00FF' }))
    canvas.add(new Textbox(layoutName.toUpperCase(), { left: 20, top: 20, width: 500, fontSize: 30, fill: '#fff', fontWeight: 'bold' }))

    if (activeSlide) {
      const text = new Textbox(activeSlide.text.toUpperCase(), {
        left: 24,
        top: 120,
        width: 492,
        fontSize: 34,
        lineHeight: 1.05,
        fill: '#ffffff',
        fontWeight: 'bold',
      })
      canvas.add(text)
    } else {
      canvas.add(new Textbox('CLIQUE EM "CARREGAR EXEMPLO GAMES"', { left: 24, top: 160, width: 492, fontSize: 28, fill: '#fff' }))
    }

    if (layoutName === 'Template Twitter') {
      canvas.add(new Rect({ left: 24, top: 430, width: 230, height: 70, fill: '#111827', rx: 10, ry: 10 }))
      canvas.add(new Textbox('@BrandsDecoded__\ncard social proof', { left: 36, top: 444, width: 210, fontSize: 16, fill: '#fff' }))
    }

    canvas.add(new Rect({ left: 0, top: 500, width: 540, height: 8, fill: selectedTheme?.palette ?? '#9D00FF' }))
    return () => canvas.dispose()
  }, [activeSlide, selectedTheme, layoutName])

  async function loadGamesExample() {
    const response = await fetch(`${API}/api/examples/games-news`)
    const data = (await response.json()) as ExampleResponse
    setExample(data)
    setRawText(data.slides.join('\n'))
    setNiche('Games')
    setTemplate(data.template)
    setSlideCount(Math.max(5, Math.min(15, data.slides.length)))
  }

  async function generate() {
    setLoading(true)
    const response = await fetch(`${API}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        niche,
        template,
        raw_text: rawText,
        slide_count: slideCount,
        assets: ['cover.jpg', 'clip1.mp4', 'shot2.jpg'],
      }),
    })
    const data = (await response.json()) as GenerateResponse
    setResult(data)
    setLoading(false)
  }

  return (
    <main>
      <h1>Instagram Carousel Studio</h1>
      <p>Sim, é possível entregar carrosséis similares ao exemplo: agora o app já inclui layouts “Template Autoral” e “Template Twitter” adaptáveis a 5–15 slides.</p>
      <section className="grid">
        <div>
          <button className="secondary" onClick={loadGamesExample}>Carregar exemplo Games</button>
          <label>Layout visual</label>
          <select value={layoutName} onChange={(e) => setLayoutName(e.target.value)}>
            <option>Template Autoral</option><option>Template Twitter</option>
          </select>
          <label>Nicho</label>
          <select value={niche} onChange={(e) => setNiche(e.target.value)}>
            <option>NFL</option><option>F1</option><option>Games</option><option>Noticias</option>
          </select>
          <label>Template narrativo</label>
          <input value={template} onChange={(e) => setTemplate(e.target.value)} />
          <label>Quantidade de slides (5-15)</label>
          <input type="number" min={5} max={15} value={slideCount} onChange={(e) => setSlideCount(Math.max(5, Math.min(15, Number(e.target.value) || 5)))} />
          <label>Texto bruto</label>
          <textarea rows={8} value={rawText} onChange={(e) => setRawText(e.target.value)} />
          <button onClick={generate} disabled={loading}>{loading ? 'Analisando...' : 'GERAR'}</button>
          {result && <p>Provider: {result.provider} | Modo mídia: {result.mode}</p>}

          {capability && (
            <article className="identity-card">
              <h3>Capacidade do projeto</h3>
              <p><strong>Consegue entregar similar?</strong> {capability.can_build_similar ? 'Sim' : 'Parcial'}</p>
              <p><strong>Faixa:</strong> {capability.supported_slide_range.join('–')} slides</p>
              <p><strong>Layouts:</strong> {capability.supported_layouts.join(', ')}</p>
            </article>
          )}

          {selectedLayout && (
            <article className="identity-card">
              <h3>{layoutName}</h3>
              <p><strong>Descrição:</strong> {selectedLayout.description}</p>
              <p><strong>Grid:</strong> {selectedLayout.identity.grid}</p>
              <p><strong>Regra inicial:</strong> {selectedLayout.rules.first_slide}</p>
            </article>
          )}

          {selectedTheme && (
            <article className="identity-card">
              <h3>Identidade do tema {niche}</h3>
              <p><strong>Headline:</strong> {selectedTheme.headline}</p>
              <p><strong>Body:</strong> {selectedTheme.body}</p>
              <p><strong>Direção:</strong> {selectedTheme.identity?.direction}</p>
              <p><strong>Referência:</strong> {selectedTheme.identity?.inspired_by}</p>
            </article>
          )}

          {example && (
            <article className="identity-card">
              <h3>{example.title}</h3>
              <p><strong>Fonte headline:</strong> {example.visual_recipe.headline_font}</p>
              <p><strong>Fonte body:</strong> {example.visual_recipe.body_font}</p>
              <p><strong>Composição:</strong> {example.visual_recipe.composition}</p>
            </article>
          )}
        </div>
        <div>
          <canvas ref={canvasRef} />
        </div>
      </section>
    </main>
  )
}
