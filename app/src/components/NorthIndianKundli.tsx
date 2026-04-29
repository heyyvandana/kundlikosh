// North Indian Kundli renderer — diamond layout, fixed houses (1 at top), signs
// rotate based on Lagna. Planets are drawn into their houses by abbreviation.
//
// The diagram is a 200x200 square with 4 outer triangles + 4 inner triangles +
// 4 small corner triangles. Houses 1..12 are positioned per classical convention.
import React from 'react';
import Svg, { G, Line, Rect, Text as SvgText } from 'react-native-svg';
import type { ChartResponse } from '@/api/types';
import { colors } from '@/theme/colors';

const SIZE = 280;
const M = 6; // padding

const PLANET_ABBR: Record<string, string> = {
  Sun: 'Su',
  Moon: 'Mo',
  Mars: 'Ma',
  Mercury: 'Me',
  Jupiter: 'Ju',
  Venus: 'Ve',
  Saturn: 'Sa',
  Rahu: 'Ra',
  Ketu: 'Ke',
};

// House center coordinates relative to a 200x200 box.
// Order: index 0 → House 1, etc. Convention matches standard North Indian kundli.
const HOUSE_XY: Array<[number, number]> = [
  [100, 50], // H1 top-center
  [50, 25], // H2 top-left
  [25, 50], // H3 left-top
  [50, 100], // H4 left-center
  [25, 150], // H5 left-bottom
  [50, 175], // H6 bottom-left
  [100, 150], // H7 bottom-center
  [150, 175], // H8 bottom-right
  [175, 150], // H9 right-bottom
  [150, 100], // H10 right-center
  [175, 50], // H11 right-top
  [150, 25], // H12 top-right
];

// House → sign offset comes from Lagna sign index. We label each house with the
// sign number (1..12), counting from Lagna.
function houseSignNumber(houseIndex: number, lagnaSignIndex: number): number {
  return ((lagnaSignIndex + houseIndex) % 12) + 1;
}

interface Props {
  chart: ChartResponse;
  size?: number;
}

export function NorthIndianKundli({ chart, size = SIZE }: Props) {
  // Group planets by house
  const byHouse: Record<number, string[]> = {};
  for (const p of chart.planets) {
    const tokens = byHouse[p.house] ?? [];
    tokens.push(`${PLANET_ABBR[p.name] ?? p.name.slice(0, 2)}${p.retrograde ? '↺' : ''}`);
    byHouse[p.house] = tokens;
  }

  // map from 200-unit grid to whatever size we render at
  const k = (size - M * 2) / 200;
  const x = (v: number) => M + v * k;
  const y = (v: number) => M + v * k;

  return (
    <Svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
      {/* parchment background */}
      <Rect x={0} y={0} width={size} height={size} fill={colors.cream} rx={6} />
      {/* outer square */}
      <Rect x={M} y={M} width={size - M * 2} height={size - M * 2} fill="none" stroke={colors.maroon} strokeWidth={1.5} />
      {/* 2 diagonals */}
      <Line x1={M} y1={M} x2={size - M} y2={size - M} stroke={colors.maroon} strokeWidth={1} />
      <Line x1={size - M} y1={M} x2={M} y2={size - M} stroke={colors.maroon} strokeWidth={1} />
      {/* inner diamond connecting midpoints */}
      <Line x1={M + (size - 2 * M) / 2} y1={M} x2={size - M} y2={M + (size - 2 * M) / 2} stroke={colors.maroon} strokeWidth={1} />
      <Line x1={size - M} y1={M + (size - 2 * M) / 2} x2={M + (size - 2 * M) / 2} y2={size - M} stroke={colors.maroon} strokeWidth={1} />
      <Line x1={M + (size - 2 * M) / 2} y1={size - M} x2={M} y2={M + (size - 2 * M) / 2} stroke={colors.maroon} strokeWidth={1} />
      <Line x1={M} y1={M + (size - 2 * M) / 2} x2={M + (size - 2 * M) / 2} y2={M} stroke={colors.maroon} strokeWidth={1} />

      {/* house labels + planets */}
      {HOUSE_XY.map(([cx, cy], i) => {
        const house = i + 1;
        const sign = houseSignNumber(i, chart.lagna_sign_index);
        const planets = byHouse[house] ?? [];
        return (
          <G key={house}>
            {/* sign number (small, italic, top of cell) */}
            <SvgText
              x={x(cx)}
              y={y(cy - 14)}
              fontSize={9}
              fontStyle="italic"
              textAnchor="middle"
              fill={colors.saffronDeep}
            >
              {sign}
            </SvgText>
            {/* planets stacked */}
            {planets.map((tok, idx) => (
              <SvgText
                key={idx}
                x={x(cx)}
                y={y(cy + (idx - (planets.length - 1) / 2) * 11)}
                fontSize={11}
                fontWeight="600"
                textAnchor="middle"
                fill={colors.maroon}
              >
                {tok}
              </SvgText>
            ))}
          </G>
        );
      })}
    </Svg>
  );
}
