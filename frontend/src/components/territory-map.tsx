"use client";

import { useEffect, useRef, useState } from "react";
import {
  AttributionControl,
  Map,
  NavigationControl,
  setWorkerUrl,
} from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";

const BASE_MAP_STYLE = "https://tiles.openfreemap.org/styles/liberty";

type MapState = "loading" | "ready" | "unavailable";

export function TerritoryMap() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [mapState, setMapState] = useState<MapState>("loading");

  useEffect(() => {
    if (!containerRef.current) {
      return;
    }

    setWorkerUrl("/maplibre/maplibre-gl-worker.mjs");

    let map: Map | undefined;
    let disposed = false;

    try {
      map = new Map({
        container: containerRef.current,
        style: BASE_MAP_STYLE,
        center: [-9.1, 39.45],
        zoom: 5.3,
        minZoom: 3,
        maxZoom: 16,
        attributionControl: false,
      });

      map.addControl(
        new NavigationControl({ showCompass: false }),
        "top-right",
      );
      map.addControl(
        new AttributionControl({ compact: true }),
        "bottom-right",
      );
      map.once("load", () => {
        if (!disposed) {
          setMapState("ready");
        }
      });
      map.once("error", () => {
        if (!disposed) {
          setMapState("unavailable");
        }
      });
    } catch {
      queueMicrotask(() => {
        if (!disposed) {
          setMapState("unavailable");
        }
      });
    }

    return () => {
      disposed = true;
      map?.remove();
    };
  }, []);

  const statusLabel =
    mapState === "ready"
      ? "Mapa base disponível"
      : mapState === "unavailable"
        ? "Mapa base indisponível"
        : "A carregar mapa base";

  return (
    <div className="relative h-full min-h-[31rem] overflow-hidden border border-[#cbd8d3] bg-[#dfe8e4] shadow-[0_8px_24px_rgba(24,51,45,0.08)]">
      <div
        ref={containerRef}
        className="absolute inset-0"
        role="region"
        aria-label="Mapa interativo de contexto de Portugal"
      />

      <div className="pointer-events-none absolute top-3 left-3 max-w-[calc(100%-5rem)] bg-white/95 p-4 shadow-[0_4px_18px_rgba(24,51,45,0.16)] backdrop-blur-sm sm:top-5 sm:left-5 sm:max-w-sm sm:p-5">
        <div className="flex items-center gap-2">
          <span className="h-2 w-2 rounded-full bg-[#c48a23]" aria-hidden="true" />
          <p className="text-xs font-semibold uppercase text-[#7b5a1d]">Preparação</p>
        </div>
        <h2 className="mt-2 text-lg font-semibold text-[#18332d]">
          Geometria territorial ainda não integrada
        </h2>
        <p className="mt-2 text-sm leading-5 text-[#536862]">
          O mapa mostra apenas contexto geográfico. Os limites administrativos
          serão adicionados quando a geometria oficial, a edição CAOP e o sistema
          de referência estiverem validados em conjunto.
        </p>
        <p className="mt-3 border-t border-[#dbe3e0] pt-3 text-xs font-medium text-[#64756f]">
          {statusLabel}
        </p>
      </div>
    </div>
  );
}
