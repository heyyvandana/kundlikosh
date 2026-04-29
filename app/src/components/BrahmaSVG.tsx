// Hand-coded geometric SVG of Brahma (4-faced creator deity on a lotus throne).
// Stylised, deliberately illustrative — no AI raster art.
// We'll add other deities (Aditi, Yama, Brihaspati...) one-by-one as users with
// those nakshatras land. For Phase 1 we need only Rohini → Brahma + a few common.
import React from 'react';
import Svg, {
  Circle,
  Defs,
  Ellipse,
  G,
  LinearGradient as SvgGrad,
  Path,
  Stop,
} from 'react-native-svg';

export function BrahmaSVG({ size = 160 }: { size?: number }) {
  return (
    <Svg width={size} height={size} viewBox="0 0 160 160">
      <Defs>
        <SvgGrad id="halo" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#E8C547" stopOpacity="1" />
          <Stop offset="1" stopColor="#C8501A" stopOpacity="0.6" />
        </SvgGrad>
        <SvgGrad id="skin" x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0" stopColor="#F8C99B" />
          <Stop offset="1" stopColor="#D89464" />
        </SvgGrad>
      </Defs>
      {/* Halo */}
      <Circle cx="80" cy="70" r="46" fill="url(#halo)" opacity="0.85" />
      <Circle cx="80" cy="70" r="46" fill="none" stroke="#8E2A0A" strokeWidth="0.8" />
      {/* Halo rays */}
      <G stroke="#8E2A0A" strokeWidth="0.6" opacity="0.7">
        {Array.from({ length: 12 }).map((_, i) => {
          const a = (i * 30 * Math.PI) / 180;
          const x1 = 80 + Math.cos(a) * 48;
          const y1 = 70 + Math.sin(a) * 48;
          const x2 = 80 + Math.cos(a) * 56;
          const y2 = 70 + Math.sin(a) * 56;
          return <Path key={i} d={`M${x1} ${y1} L${x2} ${y2}`} />;
        })}
      </G>
      {/* Lotus seat */}
      <G transform="translate(80 130)">
        {[-30, -15, 0, 15, 30].map((dx, i) => (
          <Ellipse key={i} cx={dx} cy="0" rx="14" ry="6" fill="#FBF3E2" stroke="#8E2A0A" />
        ))}
        <Ellipse cx="0" cy="-3" rx="34" ry="5" fill="#FBF3E2" stroke="#8E2A0A" />
      </G>
      {/* Body / robe */}
      <Path
        d="M55 110 Q80 95 105 110 L100 125 Q80 130 60 125 Z"
        fill="#C8501A"
        stroke="#8E2A0A"
        strokeWidth="1"
      />
      {/* Neck */}
      <Path d="M73 92 L73 102 Q80 105 87 102 L87 92 Z" fill="url(#skin)" stroke="#8E2A0A" />
      {/* Three visible faces (4th implied behind) */}
      {[-22, 0, 22].map((dx, i) => (
        <G key={i} transform={`translate(${80 + dx} 70)`}>
          <Ellipse cx="0" cy="0" rx="11" ry="13" fill="url(#skin)" stroke="#8E2A0A" strokeWidth="0.8" />
          {/* eyes */}
          <Circle cx="-3.5" cy="-1" r="0.9" fill="#5B1F00" />
          <Circle cx="3.5" cy="-1" r="0.9" fill="#5B1F00" />
          {/* third eye */}
          <Path d="M0 -5 L-1 -7 L1 -7 Z" fill="#8E2A0A" />
          {/* mouth */}
          <Path d="M-3 4 Q0 6 3 4" stroke="#5B1F00" strokeWidth="0.8" fill="none" />
          {/* beard */}
          <Path d="M-4 7 Q0 12 4 7" stroke="#5B1F00" strokeWidth="0.6" fill="#FFF8E7" />
          {/* crown */}
          <Path d="M-9 -10 L-6 -14 L-3 -10 L0 -14 L3 -10 L6 -14 L9 -10 Z"
            fill="#E8C547" stroke="#8E2A0A" strokeWidth="0.6" />
        </G>
      ))}
      {/* Arms */}
      <Path d="M55 108 Q40 95 38 78" stroke="#8E2A0A" strokeWidth="1" fill="url(#skin)" />
      <Path d="M105 108 Q120 95 122 78" stroke="#8E2A0A" strokeWidth="1" fill="url(#skin)" />
      {/* Held items: Vedas (book) + kamandalu (water-pot) */}
      <Path d="M30 70 L46 70 L46 84 L30 84 Z" fill="#FFF8E7" stroke="#8E2A0A" />
      <Path d="M38 70 L38 84" stroke="#8E2A0A" strokeWidth="0.5" />
      <Path
        d="M118 75 Q130 75 130 85 Q130 95 122 95 Q114 95 114 85 Q114 78 118 75 Z"
        fill="#C9A227"
        stroke="#8E2A0A"
      />
    </Svg>
  );
}
