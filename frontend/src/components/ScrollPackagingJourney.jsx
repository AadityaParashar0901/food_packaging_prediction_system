import { useEffect, useRef } from "react";
import { ArrowDownward, ArrowForward, AutoAwesomeOutlined } from "@mui/icons-material";
import { Button } from "@mui/material";
import "./ScrollPackagingJourney.css";

const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
const smoothstep = (start, end, value) => {
  const normalized = clamp((value - start) / (end - start));
  return normalized * normalized * (3 - 2 * normalized);
};

function SugarcaneStalk({ x, height, tilt = 0 }) {
  return (
    <g transform={`translate(${x} 0) rotate(${tilt} 0 440)`}>
      <path d={`M0 440 C-4 ${440 - height * 0.33} 5 ${440 - height * 0.66} 0 ${440 - height}`} className="journey-stalk" />
      <path d={`M0 ${440 - height * 0.45} C-24 ${420 - height * 0.52} -26 ${405 - height * 0.56} -34 ${392 - height * 0.57}`} className="journey-leaf" />
      <path d={`M0 ${440 - height * 0.6} C22 ${404 - height * 0.7} 27 ${390 - height * 0.72} 42 ${377 - height * 0.72}`} className="journey-leaf journey-leaf--light" />
    </g>
  );
}

function MaterialCube({ index }) {
  const column = index % 4;
  const row = Math.floor(index / 4);
  return (
    <div
      className="journey-cube"
      style={{ "--cube-column": column, "--cube-row": row, "--cube-index": index }}
      aria-hidden="true"
    >
      <span className="journey-cube__top" />
      <span className="journey-cube__front" />
      <span className="journey-cube__side" />
    </div>
  );
}

function JourneyVisual() {
  return (
    <div className="journey-visual" aria-label="Agricultural waste being processed into sustainable food packaging" role="img">
      <div className="journey-visual__wash" />
      <svg className="journey-svg" viewBox="0 0 760 520" focusable="false" aria-hidden="true">
        <defs>
          <linearGradient id="journey-sky" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stopColor="#f7fbff" />
            <stop offset="1" stopColor="#eef6f0" />
          </linearGradient>
          <linearGradient id="journey-machine" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#f5fbff" />
            <stop offset="1" stopColor="#d8e7f2" />
          </linearGradient>
          <linearGradient id="journey-factory" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stopColor="#ffffff" />
            <stop offset="1" stopColor="#dfeaf2" />
          </linearGradient>
          <pattern id="journey-fiber" width="18" height="14" patternUnits="userSpaceOnUse">
            <path d="M1 8 C5 2 7 12 12 5 S17 7 20 2" fill="none" stroke="#92b78e" strokeWidth="1.6" opacity=".55" />
            <path d="M-3 13 C3 8 8 16 13 10" fill="none" stroke="#d2dfc7" strokeWidth="1.2" opacity=".9" />
          </pattern>
          <filter id="journey-shadow" x="-20%" y="-20%" width="140%" height="160%">
            <feDropShadow dx="0" dy="9" stdDeviation="8" floodColor="#17324d" floodOpacity=".12" />
          </filter>
        </defs>

        <rect x="18" y="18" width="724" height="466" rx="28" fill="url(#journey-sky)" />
        <path d="M18 372 C150 330 244 350 350 365 S584 340 742 362 V484 H18Z" fill="#e7f2e7" />
        <path d="M18 414 C182 383 277 408 390 414 S598 390 742 408 V484 H18Z" fill="#d6e9d5" />

        <g className="journey-scene journey-scene--farm">
          <g className="journey-sugarcane">
            <SugarcaneStalk x={90} height={162} tilt={-3} />
            <SugarcaneStalk x={130} height={186} tilt={4} />
            <SugarcaneStalk x={177} height={145} tilt={-7} />
            <SugarcaneStalk x={220} height={198} tilt={6} />
            <SugarcaneStalk x={265} height={160} tilt={-4} />
          </g>
          <g className="journey-farmer" transform="translate(54 286)">
            <circle cx="24" cy="20" r="14" fill="#c8825a" />
            <path d="M8 16 C13 0 37 0 43 17 C32 13 19 13 8 16Z" fill="#294f42" />
            <path d="M10 42 C20 34 32 34 41 42 L51 91 H0Z" fill="#1976d2" />
            <path d="M12 89 L6 135 M38 89 L46 135" stroke="#38576b" strokeWidth="10" strokeLinecap="round" />
            <path d="M5 135 H-4 M45 135 H55" stroke="#38576b" strokeWidth="7" strokeLinecap="round" />
            <path d="M5 48 L-12 80 M45 48 L70 69" stroke="#c8825a" strokeWidth="9" strokeLinecap="round" />
            <path d="M66 67 L93 61" stroke="#6b472e" strokeWidth="4" strokeLinecap="round" />
          </g>
          <g className="journey-machine" transform="translate(292 282)" filter="url(#journey-shadow)">
            <path d="M9 50 H220 L242 166 H0Z" fill="url(#journey-machine)" stroke="#507187" strokeWidth="3" />
            <path d="M27 51 H206 V20 H27Z" fill="#d5e5ed" stroke="#507187" strokeWidth="3" />
            <path d="M48 20 L61 3 H169 L185 20Z" fill="#eaf4f8" stroke="#507187" strokeWidth="3" />
            <circle cx="84" cy="101" r="34" fill="#a8c0cb" stroke="#436579" strokeWidth="4" />
            <circle cx="151" cy="101" r="34" fill="#a8c0cb" stroke="#436579" strokeWidth="4" />
            <path d="M55 101 H181" stroke="#436579" strokeWidth="7" strokeDasharray="10 8" />
            <path d="M84 74 V128 M57 89 L111 113 M57 113 L111 89 M151 74 V128 M124 89 L178 113 M124 113 L178 89" stroke="#f8fcfd" strokeWidth="4" opacity=".9" />
            <rect x="25" y="137" width="194" height="18" rx="9" fill="#1976d2" opacity=".18" />
            <circle cx="25" cy="169" r="9" fill="#567889" /><circle cx="215" cy="169" r="9" fill="#567889" />
          </g>
          <path className="journey-feed" d="M238 362 C258 362 270 360 292 353" />
          <path className="journey-waste" d="M536 360 C568 359 585 357 611 348" />
          <g className="journey-waste-pile" transform="translate(606 348)">
            <path d="M0 31 C3 4 23 -4 40 14 C50 -10 75 0 76 28Z" fill="#a7bf83" stroke="#66815f" strokeWidth="3" />
            <path d="M18 26 L39 8 M38 30 L58 12 M53 31 L70 18" stroke="#e0e8c8" strokeWidth="4" strokeLinecap="round" />
          </g>
        </g>

        <g className="journey-scene journey-scene--bridge">
          <path className="journey-route" d="M312 369 C408 426 494 421 625 348" />
          <path className="journey-route journey-route--accent" d="M312 369 C408 426 494 421 625 348" />
          <g className="journey-bridge-waste">
            <path d="M0 -12 C10 -30 30 -29 39 -12 C53 -26 73 -12 70 6 C64 24 38 25 21 16 C8 24 -4 9 0 -12Z" fill="#a7bf83" stroke="#66815f" strokeWidth="3" />
            <path d="M13 4 L29 -12 M30 13 L48 -6 M45 12 L60 0" stroke="#e0e8c8" strokeWidth="4" strokeLinecap="round" />
          </g>
          <g className="journey-factory-small" transform="translate(562 226)">
            <path d="M0 142 V54 L44 24 L87 54 V142Z" fill="url(#journey-factory)" stroke="#527086" strokeWidth="3" />
            <path d="M44 24 V0 M50 24 V0" stroke="#527086" strokeWidth="5" />
            <path d="M19 75 H71 M19 101 H71" stroke="#9db8c7" strokeWidth="8" />
            <rect x="28" y="119" width="30" height="23" rx="4" fill="#1976d2" opacity=".75" />
          </g>
        </g>

        <g className="journey-scene journey-scene--factory" filter="url(#journey-shadow)">
          <path d="M72 387 V170 L144 119 L217 170 V387Z" fill="url(#journey-factory)" stroke="#527086" strokeWidth="3" />
          <path d="M145 119 V75 M152 119 V75" stroke="#527086" strokeWidth="7" />
          <path d="M124 169 H190 M124 202 H190 M124 235 H190" stroke="#b6cad6" strokeWidth="12" />
          <rect x="99" y="272" width="90" height="84" rx="8" fill="#edf4f6" stroke="#668398" strokeWidth="3" />
          <circle cx="126" cy="315" r="11" fill="#7da1b3" /><circle cx="161" cy="315" r="11" fill="#7da1b3" />
          <path d="M217 340 H581" stroke="#557487" strokeWidth="18" strokeLinecap="round" />
          <path d="M230 340 H568" stroke="#dce8ed" strokeWidth="9" strokeDasharray="16 12" />
          <path d="M276 281 H367 V331 H276Z" fill="#cfe0e7" stroke="#557487" strokeWidth="3" />
          <path d="M290 281 L299 248 H345 L355 281Z" fill="#eaf4f6" stroke="#557487" strokeWidth="3" />
          <circle cx="309" cy="306" r="18" fill="#a8c0cb" stroke="#557487" strokeWidth="3" /><circle cx="343" cy="306" r="18" fill="#a8c0cb" stroke="#557487" strokeWidth="3" />
          <path d="M438 267 H527 V334 H438Z" fill="#d9e6eb" stroke="#557487" strokeWidth="3" />
          <path d="M451 267 V239 H514 V267Z" fill="#eef5f7" stroke="#557487" strokeWidth="3" />
          <path d="M452 296 H513 M452 317 H513" stroke="#1976d2" strokeWidth="6" opacity=".7" />
          <g className="journey-particles"><circle cx="252" cy="318" r="5" /><circle cx="397" cy="339" r="4" /><circle cx="413" cy="324" r="6" /><circle cx="551" cy="319" r="5" /></g>
          <g className="journey-factory-blocks"><rect x="574" y="307" width="25" height="25" rx="4" /><rect x="605" y="307" width="25" height="25" rx="4" /><rect x="636" y="307" width="25" height="25" rx="4" /></g>
        </g>

        <g className="journey-scene journey-scene--material">
          <ellipse cx="380" cy="421" rx="190" ry="22" fill="#dfe9e5" />
          <g className="journey-single-block" transform="translate(307 242)">
            <path d="M0 56 L72 28 L145 56 L72 84Z" fill="#bcd3aa" stroke="#64825f" strokeWidth="3" />
            <path d="M0 56 V166 L72 198 V84Z" fill="#9fbe91" stroke="#64825f" strokeWidth="3" />
            <path d="M145 56 V166 L72 198 V84Z" fill="#86ac82" stroke="#64825f" strokeWidth="3" />
            <path d="M0 56 L72 28 L145 56 L72 84Z M0 56 V166 L72 198 V84Z M145 56 V166 L72 198 V84Z" fill="url(#journey-fiber)" opacity=".6" />
            <path d="M28 62 L71 45 M39 151 L67 166 M101 144 L129 125" stroke="#e8f0dd" strokeWidth="4" strokeLinecap="round" opacity=".7" />
          </g>
          <g className="journey-material-label"><rect x="264" y="451" width="232" height="24" rx="12" fill="#ffffff" opacity=".9" /><text x="380" y="468" textAnchor="middle">PROCESSED FIBER MATERIAL</text></g>
        </g>

        <g className="journey-scene journey-scene--sheet">
          <path className="journey-sheet-shadow" d="M168 402 L381 342 L594 402 L381 462Z" />
          <path className="journey-sheet" d="M168 368 L381 308 L594 368 L381 428Z" fill="url(#journey-fiber)" stroke="#64825f" strokeWidth="4" />
          <path d="M215 365 L382 319 M282 389 L462 338 M365 414 L545 365" stroke="#ffffff" strokeWidth="5" opacity=".65" strokeLinecap="round" />
          <path d="M191 384 C284 354 381 348 571 382" fill="none" stroke="#1976d2" strokeWidth="3" strokeDasharray="7 10" opacity=".65" />
          <text x="381" y="468" textAnchor="middle">FIBER-BASED PACKAGING SHEET</text>
        </g>

        <g className="journey-scene journey-scene--package">
          <ellipse cx="380" cy="424" rx="206" ry="25" fill="#dfe9e5" />
          <path d="M205 364 L380 320 L555 364 L380 410Z" fill="#b9d4ad" stroke="#64825f" strokeWidth="4" />
          <path d="M205 364 V397 L380 448 V410Z" fill="#94b888" stroke="#64825f" strokeWidth="4" />
          <path d="M555 364 V397 L380 448 V410Z" fill="#7fa478" stroke="#64825f" strokeWidth="4" />
          <path d="M205 364 L380 320 L555 364 L380 410Z" fill="url(#journey-fiber)" opacity=".65" />
          <path d="M270 368 L380 341 L490 368 L380 396Z" fill="#ffffff" opacity=".88" />
          <path d="M301 367 L380 348 L459 367 L380 386Z" fill="#e7f1e5" stroke="#1976d2" strokeWidth="2" opacity=".9" />
          <path d="M380 355 L380 379 M368 369 H392" stroke="#1976d2" strokeWidth="2.5" />
          <text x="380" y="429" textAnchor="middle" className="journey-package-text">FRESH PRODUCE</text>
          <text x="380" y="477" textAnchor="middle">AGRICULTURAL WASTE, REIMAGINED</text>
        </g>
      </svg>

      <div className="journey-grid" aria-hidden="true">
        {Array.from({ length: 16 }, (_, index) => <MaterialCube key={index} index={index} />)}
      </div>
      <div className="journey-visual__caption">Agricultural waste <ArrowForward /> useful material <ArrowForward /> food packaging</div>
    </div>
  );
}

export default function ScrollPackagingJourney() {
  const journeyRef = useRef(null);
  const visualRef = useRef(null);

  useEffect(() => {
    const journey = journeyRef.current;
    const visual = visualRef.current;
    if (!journey || !visual) return undefined;

    let frame = 0;
    const render = () => {
      frame = 0;
      const rect = journey.getBoundingClientRect();
      const travel = Math.max(journey.offsetHeight - window.innerHeight, 1);
      const progress = clamp(-rect.top / travel);
      const values = {
        progress,
        farm: clamp(1 - smoothstep(0.1, 0.31, progress)),
        bridge: smoothstep(0.12, 0.37, progress) * (1 - smoothstep(0.31, 0.48, progress)),
        factory: smoothstep(0.27, 0.45, progress) * (1 - smoothstep(0.48, 0.63, progress)),
        material: smoothstep(0.48, 0.65, progress) * (1 - smoothstep(0.73, 0.82, progress)),
        grid: smoothstep(0.59, 0.79, progress) * (1 - smoothstep(0.78, 0.91, progress)),
        sheet: smoothstep(0.74, 0.9, progress) * (1 - smoothstep(0.88, 0.96, progress)),
        package: smoothstep(0.87, 1, progress),
      };
      Object.entries(values).forEach(([name, value]) => visual.style.setProperty(`--journey-${name}`, value));
    };
    const requestRender = () => { if (!frame) frame = window.requestAnimationFrame(render); };
    render();
    window.addEventListener("scroll", requestRender, { passive: true });
    window.addEventListener("resize", requestRender);
    return () => {
      window.removeEventListener("scroll", requestRender);
      window.removeEventListener("resize", requestRender);
      if (frame) window.cancelAnimationFrame(frame);
    };
  }, []);

  return (
    <section className="packaging-journey" ref={journeyRef} aria-labelledby="journey-title">
      <div className="packaging-journey__sticky">
        <div className="packaging-journey__visual-wrap" ref={visualRef}>
          <JourneyVisual />
          <div className="journey-progress" aria-hidden="true"><span /><span /><span /><span /><span /><span /><span /></div>
        </div>
        <div className="packaging-journey__copy">
          <div className="packaging-journey__eyebrow"><AutoAwesomeOutlined /> MATERIAL JOURNEY</div>
          <h1 id="journey-title">Smarter Packaging.<br />Sustainable by Design.</h1>
          <p>Discover packaging solutions designed around food properties, storage conditions, and sustainable material choices.</p>
          <Button variant="contained" href="#food-storage-profile" endIcon={<ArrowDownward />}>
            Get Started
          </Button>
          <div className="packaging-journey__stages" aria-hidden="true">
            <span>Farm</span><i /><span>Process</span><i /><span>Form</span><i /><span>Protect</span>
          </div>
        </div>
      </div>
    </section>
  );
}
