#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
05_arquitectura/AR03_brechas.py
Análisis cuantitativo de Brechas de Arquitectura Empresarial y Derivación de Paquetes de Trabajo
SI-886 · Planeamiento Estratégico de TI · Semana 10 · Taller de Laboratorio
Organización: CrediTech Perú S.A.C. | RUC: 20608945123
Autor: Ramos Atahuachi, Fabricio Farid Edmilson (2023076798)
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def main():
    # Asegurar codificación utf-8 en terminal
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass

    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))
    csv_path = os.path.join(base_dir, "AR03_brechas.csv")
    out_txt_dir = os.path.join(root_dir, "docs", "evidencias", "S10", "salidas")
    out_graf_dir = os.path.join(root_dir, "graficos")

    os.makedirs(out_txt_dir, exist_ok=True)
    os.makedirs(out_graf_dir, exist_ok=True)

    if not os.path.exists(csv_path):
        print(f"Error: no se encontró {csv_path}")
        return

    df = pd.read_csv(csv_path)
    total_brechas = len(df)

    salida_lineas = []
    def log(msg=""):
        print(msg)
        salida_lineas.append(msg)

    log("=" * 85)
    log("  REPORTE DE ANÁLISIS DE BRECHAS DE ARQUITECTURA EMPRESARIAL — PETI v0.10")
    log("  ORGANIZACIÓN: CrediTech Perú S.A.C. | RUC: 20608945123")
    log("  ESTUDIANTE: Ramos Atahuachi, Fabricio Farid Edmilson (2023076798)")
    log("=" * 85)
    log()

    # 1. Resumen Cuantitativo por Capa
    capa_counts = df["Capa"].value_counts()
    capa_pct = (df["Capa"].value_counts(normalize=True) * 100).round(1)
    resumen_capa = pd.DataFrame({"Cantidad": capa_counts, "Porcentaje (%)": capa_pct})
    log("--- 1. DISTRIBUCIÓN DE BRECHAS POR CAPA DE ARQUITECTURA (N = {}) ---".format(total_brechas))
    log(resumen_capa.to_string())
    log()

    # 2. Resumen Cuantitativo por Tipo de Brecha
    tipo_counts = df["Tipo_Brecha"].value_counts()
    tipo_pct = (df["Tipo_Brecha"].value_counts(normalize=True) * 100).round(1)
    resumen_tipo = pd.DataFrame({"Cantidad": tipo_counts, "Porcentaje (%)": tipo_pct})
    log("--- 2. DISTRIBUCIÓN POR TIPO DE BRECHA (TOGAF / ARCHIMATE) ---")
    log(resumen_tipo.to_string())
    log()

    # 3. Resumen Cuantitativo por Esfuerzo y Prioridad
    esfuerzo_counts = df["Esfuerzo"].value_counts()
    prioridad_counts = df["Prioridad"].value_counts()
    log("--- 3. ESTIMACIÓN DE ESFUERZO Y PRIORIDAD ESTRATÉGICA ---")
    log("Esfuerzo estimado:")
    for k, v in esfuerzo_counts.items():
        log(f"  • {k:8s}: {v:2d} brechas ({v/total_brechas*100:.1f} %)")
    log("Prioridad de atención:")
    for k, v in prioridad_counts.items():
        log(f"  • {k:8s}: {v:2d} brechas ({v/total_brechas*100:.1f} %)")
    log()

    # 4. Tabla de Brechas y Elementos
    log("--- 4. MATRIZ DETALLADA DE BRECHAS POR CAPA ---")
    for idx, row in df.iterrows():
        log(f"[{row['ID']}] ({row['Capa']}) Tipo: {row['Tipo_Brecha']} | Esfuerzo: {row['Esfuerzo']} | Prioridad: {row['Prioridad']}")
        log(f"  As-Is : {row['Elemento_Actual']}")
        log(f"  To-Be : {row['Elemento_Objetivo']}")
        log(f"  Dep.  : {row['Dependencias']} --> Asignado a: {row['Paquete_Trabajo']}")
        log()

    # 5. Derivación de Paquetes de Trabajo
    paquetes = {}
    for idx, row in df.iterrows():
        pkg = row["Paquete_Trabajo"]
        if pkg not in paquetes:
            paquetes[pkg] = {
                "brechas": [],
                "capas": set(),
                "esfuerzos": [],
                "prioridades": [],
                "dependencias_gaps": set()
            }
        paquetes[pkg]["brechas"].append(row["ID"])
        paquetes[pkg]["capas"].add(row["Capa"])
        paquetes[pkg]["esfuerzos"].append(row["Esfuerzo"])
        paquetes[pkg]["prioridades"].append(row["Prioridad"])
        deps = [d.strip() for d in str(row["Dependencias"]).split(";") if d.strip() != "Ninguna"]
        for d in deps:
            paquetes[pkg]["dependencias_gaps"].add(d)

    log("=" * 85)
    log("--- 5. PAQUETES DE TRABAJO DERIVADOS (INSUMO DEL PORTAFOLIO SECCIÓN 7.1) ---")
    log("=" * 85)
    
    pkg_summary = []
    # Mapeo de GAP a Paquete
    gap_to_pkg = {}
    for idx, row in df.iterrows():
        gap_to_pkg[row["ID"]] = row["Paquete_Trabajo"].split()[0]

    for pkg_name, data in sorted(paquetes.items()):
        pkg_id = pkg_name.split()[0]
        # Determinar dependencias a nivel de paquete
        pkg_deps = set()
        for g_dep in data["dependencias_gaps"]:
            if g_dep in gap_to_pkg and gap_to_pkg[g_dep] != pkg_id:
                pkg_deps.add(gap_to_pkg[g_dep])
        
        # Esfuerzo consolidado (si hay Alto -> Alto, sino Medio, sino Bajo)
        esf_cons = "Alto" if "Alto" in data["esfuerzos"] else ("Medio" if "Medio" in data["esfuerzos"] else "Bajo")
        prio_cons = "Crítica" if "Crítica" in data["prioridades"] else ("Alta" if "Alta" in data["prioridades"] else "Media")
        
        data["pkg_deps"] = pkg_deps
        data["esfuerzo_cons"] = esf_cons
        data["prio_cons"] = prio_cons

        deps_str = ", ".join(sorted(pkg_deps)) if pkg_deps else "Ninguna (Habilitador Inicial)"
        log(f"• {pkg_name}")
        log(f"   Brechas que cierra : {', '.join(data['brechas'])}")
        log(f"   Capas impactadas   : {', '.join(sorted(data['capas']))}")
        log(f"   Esfuerzo / Prio    : {esf_cons} / {prio_cons}")
        log(f"   Dependencias PKG   : {deps_str}")
        log()

        pkg_summary.append({
            "Paquete": pkg_name,
            "Brechas": len(data["brechas"]),
            "Esfuerzo": esf_cons,
            "Prioridad": prio_cons,
            "Dependencias": deps_str
        })

    # 6. Secuencia Obligada por Dependencias (Roadmap / Fases de Implementación)
    log("=" * 85)
    log("--- 6. SECUENCIA OBLIGADA DE EJECUCIÓN (ANÁLISIS DE DEPENDENCIAS Y PRELACIÓN) ---")
    log("=" * 85)
    
    fases = {
        "Fase 1 · Cimientos y Habilitadores de Datos e Infraestructura": [
            ("PT-01", "Gobierno del Dato y Maestro de Clientes MDM", "Cierra GAP-03 (Sin dependencias previas. Habilita consistencia de datos)"),
            ("PT-07", "Capa de Integración API Gateway y Microservicios", "Cierra GAP-10 (Sin dependencias previas. Habilita desacoplamiento y APIs mTLS)"),
            ("PT-08", "Infraestructura Cloud Multi-AZ y DRP", "Cierra GAP-12, GAP-13 (Sin dependencias previas. Habilita resiliencia y base para ERP Cloud)")
        ],
        "Fase 2 · Cumplimiento Regulatorio Crítico y Seguridad Reforzada": [
            ("PT-02", "Privacidad de Datos y Cumplimiento Normativo ANPD", "Cierra GAP-04 (Requiere PT-01: No se puede registrar tratamiento sin maestro de clientes)"),
            ("PT-03", "Firma Digital PKI Acreditada y Bóveda de Pagarés", "Cierra GAP-05, GAP-11 (Requiere PT-01 y PT-07: Consume maestro y viaja por API Gateway)"),
            ("PT-09", "Monitoreo Centralizado SIEM/SOC 24/7", "Cierra GAP-14 (Requiere PT-08: Monitorea la infraestructura Aurora Multi-AZ y servicios nube)")
        ],
        "Fase 3 · Transformación de Procesos Core y Erradicación de Shadow IT": [
            ("PT-06", "Modernización de Scoring API v2 y Explicabilidad", "Cierra GAP-07 (Requiere PT-01 y PT-07: Consume datos limpios y expone servicio síncrono)"),
            ("PT-04", "Plataforma CRM/BPM Cobranzas y Retiro Shadow IT", "Cierra GAP-02, GAP-06, GAP-08 (Requiere PT-01, PT-07 y scoring; desmantela Excel HC-01 y HC-04)"),
            ("PT-05", "Mesa de Servicio ITSM y Reclamos Integrado SBS", "Cierra GAP-01, GAP-09 (Requiere PT-07: Conexión con portales y sistemas de atención)")
        ]
    }

    for fase_nombre, items in fases.items():
        log(f"\n{fase_nombre.upper()}:")
        for p_id, p_desc, just in items:
            log(f"  [+] {p_id}: {p_desc}")
            log(f"      Justificación técnica: {just}")

    log("\n" + "=" * 85)
    log("  JUSTIFICACIÓN ARQUITECTÓNICA DE LA SECUENCIA DE TRANSICIÓN:")
    log("  1. No es viable ejecutar analítica ni scoring v2 antes de estabilizar el Maestro de Clientes (PT-01),")
    log("     de lo contrario los modelos de Machine Learning entrenarán con datos contradictorios o duplicados.")
    log("  2. No se puede desmantelar el Shadow IT (hojas de cálculo de cobranzas HC-01 y scoring HC-04)")
    log("     antes de desplegar la plataforma CRM/BPM (PT-04) y el nuevo motor API (PT-06), pues el negocio quedaría")
    log("     sin capacidad operativa para gestionar su cartera morosa.")
    log("  3. El API Gateway (PT-07) es prerrequisito de integración para la firma digital (PT-03), el CRM de cobranzas")
    log("     (PT-04) y el sistema de reclamos (PT-05), garantizando seguridad perimetral y trazabilidad de transacciones.")
    log("=" * 85)

    # Guardar salida en archivo de texto
    out_txt_file = os.path.join(out_txt_dir, "salida_analisis_brechas.txt")
    with open(out_txt_file, "w", encoding="utf-8") as f:
        f.write("\n".join(salida_lineas) + "\n")
    print(f"\n[OK] Salida textual guardada en: {out_txt_file}")

    # =========================================================================
    # GENERACIÓN DE GRÁFICOS ANALÍTICOS (ALTA RESOLUCIÓN)
    # =========================================================================
    generar_graficos(df, out_graf_dir)

def generar_graficos(df, out_dir):
    # Paleta corporativa elegante
    c_primario = "#1A365D"    # Azul marino institucional
    c_secundario = "#2B6CB0"  # Azul pizarra
    c_acento = "#DD6B20"      # Naranja cálido
    c_verde = "#276749"       # Verde esmeralda
    c_rojo = "#9B2C2C"        # Rojo carmesí
    c_fondo = "#F7FAFC"

    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['axes.edgecolor'] = '#CBD5E0'
    plt.rcParams['axes.linewidth'] = 0.8

    # -------------------------------------------------------------------------
    # Gráfico 1: Brechas por Capa y Tipo (Barra apilada)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5), facecolor='white')
    ax.set_facecolor(c_fondo)

    # Pivot table Capa vs Tipo_Brecha
    capa_order = ["Negocio", "Datos", "Aplicación", "Tecnología"]
    tipo_order = ["Nuevo", "Modificado", "Retirado"]
    color_map = {"Nuevo": "#3182CE", "Modificado": "#DD6B20", "Retirado": "#E53E3E"}

    pivot = df.pivot_table(index="Capa", columns="Tipo_Brecha", values="ID", aggfunc="count", fill_value=0)
    pivot = pivot.reindex(capa_order).fillna(0)
    for col in tipo_order:
        if col not in pivot.columns:
            pivot[col] = 0
    pivot = pivot[tipo_order]

    bottom = np.zeros(len(capa_order))
    for tipo in tipo_order:
        values = pivot[tipo].values
        p = ax.bar(capa_order, values, bottom=bottom, label=tipo, color=color_map[tipo], width=0.55, edgecolor="white", linewidth=1.5)
        # Añadir etiquetas en las barras
        for idx, val in enumerate(values):
            if val > 0:
                ax.text(idx, bottom[idx] + val / 2, f"{int(val)}", ha='center', va='center', color='white', fontweight='bold', fontsize=11)
        bottom += values

    # Totales arriba de cada barra
    for idx, total in enumerate(bottom):
        ax.text(idx, total + 0.15, f"Total: {int(total)}", ha='center', va='bottom', color='#2D3748', fontweight='bold', fontsize=11)

    ax.set_title("CrediTech Perú S.A.C. · Brechas de Arquitectura por Capa y Tipo (N=14)", fontsize=13, fontweight='bold', pad=15, color=c_primario)
    ax.set_xlabel("Capas de Arquitectura Empresarial (ArchiMate 3.2)", fontsize=11, fontweight='bold', labelpad=10, color=c_primario)
    ax.set_ylabel("Cantidad de Brechas Identificadas", fontsize=11, fontweight='bold', labelpad=10, color=c_primario)
    ax.set_ylim(0, max(bottom) + 1.2)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(title="Tipo de Brecha", frameon=True, facecolor="white", edgecolor="#CBD5E0", loc="upper left")

    plt.tight_layout()
    g1_path = os.path.join(out_dir, "AR_brechas_por_capa.png")
    plt.savefig(g1_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 1 guardado en: {g1_path}")

    # -------------------------------------------------------------------------
    # Gráfico 2: Secuencia y Roadmap de Paquetes de Trabajo
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 6.5), facecolor='white')
    ax.set_facecolor("#FFFFFF")
    ax.axis('off')

    ax.text(6, 9.5, "SECUENCIA OBLIGADA DE PAQUETES DE TRABAJO (ROADMAP PETI)", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=c_primario)
    ax.text(6, 9.0, "Prelación algorítmica por dependencias técnicas y requerimientos regulatorios", 
            ha='center', va='center', fontsize=10.5, style='italic', color='#4A5568')

    fases_info = [
        ("FASE 1: HABILITADORES BASE", "#EBF8FF", "#2B6CB0", 8.2, 5.8, [
            ("PT-01", "Gobierno del Dato & Maestro MDM", "Cierra GAP-03\nSin dependencias"),
            ("PT-07", "API Gateway & Microservicios", "Cierra GAP-10\nSin dependencias"),
            ("PT-08", "Infraestructura Cloud Multi-AZ", "Cierra GAP-12, GAP-13\nSin dependencias")
        ]),
        ("FASE 2: SEGURIDAD Y NORMATIVA", "#FEEBC8", "#C05621", 5.2, 2.8, [
            ("PT-02", "Privacidad & RAT ANPD", "Cierra GAP-04\nDepende de PT-01"),
            ("PT-03", "Firma PKI & Bóveda Pagarés", "Cierra GAP-05, GAP-11\nDepende de PT-01, PT-07"),
            ("PT-09", "Ciberseguridad SIEM/SOC 24/7", "Cierra GAP-14\nDepende de PT-08")
        ]),
        ("FASE 3: TRANSFORMACIÓN CORE", "#C6F6D5", "#22543D", 2.2, -0.2, [
            ("PT-06", "Scoring API v2 & Explicabilidad", "Cierra GAP-07\nDepende de PT-01, PT-07"),
            ("PT-04", "CRM Cobranzas & Retiro Excel", "Cierra GAP-02, 06, 08\nDepende de PT-01, PT-07, 06"),
            ("PT-05", "ITSM Reclamos Integrado SBS", "Cierra GAP-01, GAP-09\nDepende de PT-07")
        ])
    ]

    for titulo, color_bg, color_border, y_top, y_bot, paquetes in fases_info:
        # Dibujar contenedor de fase
        rect_fase = patches.FancyBboxPatch((0.5, y_bot), 11, y_top - y_bot, 
                                           boxstyle="round,pad=0.15", 
                                           linewidth=1.5, edgecolor=color_border, facecolor=color_bg)
        ax.add_patch(rect_fase)
        ax.text(0.8, y_top - 0.35, titulo, fontsize=11, fontweight='bold', color=color_border)

        # Dibujar cajas de paquetes
        x_coords = [1.0, 4.6, 8.2]
        for idx, (p_id, p_nom, p_det) in enumerate(paquetes):
            x = x_coords[idx]
            y = y_bot + 0.3
            card = patches.FancyBboxPatch((x, y), 3.2, 1.6, 
                                          boxstyle="round,pad=0.1", 
                                          linewidth=1.2, edgecolor=color_border, facecolor="white")
            ax.add_patch(card)
            ax.text(x + 1.6, y + 1.25, p_id, ha='center', va='center', fontsize=10.5, fontweight='bold', color=color_border)
            ax.text(x + 1.6, y + 0.85, p_nom, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#2D3748')
            ax.text(x + 1.6, y + 0.35, p_det, ha='center', va='center', fontsize=7.5, color='#718096')

    # Flechas de conexión entre fases
    ax.annotate('', xy=(6, 5.3), xytext=(6, 5.7),
                arrowprops=dict(facecolor='#4A5568', edgecolor='#4A5568', width=2, headwidth=8))
    ax.annotate('', xy=(6, 2.3), xytext=(6, 2.7),
                arrowprops=dict(facecolor='#4A5568', edgecolor='#4A5568', width=2, headwidth=8))

    ax.set_xlim(0, 12)
    ax.set_ylim(-0.5, 10)

    plt.tight_layout()
    g2_path = os.path.join(out_dir, "AR_secuencia_paquetes_trabajo.png")
    plt.savefig(g2_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 2 guardado en: {g2_path}")

    # -------------------------------------------------------------------------
    # Gráfico 3: Cooperación Proceso-Aplicación (Visual Diagram)
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 7.5), facecolor='white')
    ax.set_facecolor("#FFFFFF")
    ax.axis('off')

    ax.text(5.5, 10.5, "VISTA DE COOPERACIÓN PROCESO - APLICACIÓN (AS-IS)", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=c_primario)
    ax.text(5.5, 10.0, "Evaluación de Cobertura de Sistemas y Detección de Procesos en Riesgo / Shadow IT", 
            ha='center', va='center', fontsize=10.5, style='italic', color='#4A5568')

    filas = [
        ("Toma de Solicitud y Onboarding", "Portal Web + App Móvil (incompletos) + Teléfono", "Parcial (~)", "#DD6B20", "#ED8936"),
        ("Evaluación y Scoring de Riesgo", "Motor Python batch + HOJA EXCEL SCORING (HC-04)", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Formalización Contractual", "OTP SMS simple + Core Créditos (sin firma PKI)", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Desembolso y Liquidación", "Core de Créditos + Digitación manual en Banca Web", "Parcial (~)", "#DD6B20", "#ED8936"),
        ("Facturación y Comprobantes", "ERP Contable Local (Concar)", "Bueno (✓)", "#38A169", "#276749"),
        ("Ruteo y Cobranza Preventiva", "HOJA DE CÁLCULO DE MORA (HC-01) + WhatsApp", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Gestión de Mora Prejudicial", "HOJA DE CÁLCULO (HC-01) + Llamadas manuales", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Atención de Reclamos", "Buzón Outlook Compartido (sin tickets ni SLA)", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Conciliación y Tesorería", "HOJA DE CÁLCULO CONCILIACIÓN BANCARIA (HC-03)", "Deficiente (✗)", "#E53E3E", "#C53030"),
        ("Análisis Financiero y Portafolio", "HOJAS EXCEL MÚLTIPLES + Exportación CSV", "Deficiente (✗)", "#E53E3E", "#C53030")
    ]

    # Encabezados
    ax.text(0.5, 9.3, "PROCESO DE NEGOCIO", fontsize=10.5, fontweight='bold', color=c_primario)
    ax.text(4.2, 9.3, "SISTEMA QUE LO SOPORTA", fontsize=10.5, fontweight='bold', color=c_primario)
    ax.text(8.8, 9.3, "NIVEL DE SOPORTE", fontsize=10.5, fontweight='bold', color=c_primario)
    ax.plot([0.3, 10.7], [9.1, 9.1], color=c_primario, linewidth=1.5)

    y_pos = 8.5
    for proc, sist, nivel, bg_badge, fg_badge in filas:
        # Fila fondo alterno
        card = patches.FancyBboxPatch((0.3, y_pos - 0.25), 10.4, 0.65, 
                                      boxstyle="round,pad=0.05", 
                                      linewidth=0.5, edgecolor="#E2E8F0", facecolor="#F7FAFC" if (y_pos*2)%2==0 else "#EDF2F7")
        ax.add_patch(card)
        ax.text(0.5, y_pos + 0.05, proc, fontsize=9.5, fontweight='bold', color='#2D3748', va='center')
        
        # Resaltar si es hoja de cálculo
        if "HOJA" in sist:
            ax.text(4.2, y_pos + 0.05, sist, fontsize=9, fontweight='bold', color='#C53030', va='center')
        else:
            ax.text(4.2, y_pos + 0.05, sist, fontsize=9, color='#4A5568', va='center')

        # Badge de nivel
        badge = patches.FancyBboxPatch((8.8, y_pos - 0.15), 1.7, 0.45, 
                                       boxstyle="round,pad=0.08", 
                                       linewidth=0, facecolor=bg_badge)
        ax.add_patch(badge)
        ax.text(9.65, y_pos + 0.07, nivel, ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

        y_pos -= 0.8

    # Resumen cuantitativo al pie
    resumen_text = "DIAGNÓSTICO EJECUTIVO: 7 de 10 procesos (70 %) operan sin soporte adecuado o sobre Hojas de Cálculo (Shadow IT). Solo 1 proceso (10 %) tiene soporte bueno."
    ax.text(5.5, y_pos + 0.1, resumen_text, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#C53030',
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#FFF5F5", edgecolor="#FEB2B2", linewidth=1.2))

    ax.set_xlim(0, 11)
    ax.set_ylim(0.5, 11.2)

    plt.tight_layout()
    g3_path = os.path.join(out_dir, "AR_cooperacion_proceso_aplicacion.png")
    plt.savefig(g3_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 3 guardado en: {g3_path}")

    # -------------------------------------------------------------------------
    # Gráfico 4: Arquitectura Actual (As-Is) - 3 Capas
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 8), facecolor='white')
    ax.set_facecolor("#FFFFFF")
    ax.axis('off')

    ax.text(5.5, 11.4, "ARQUITECTURA EMPRESARIAL ACTUAL (AS-IS) · CREDITECH PERÚ", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=c_primario)
    ax.text(5.5, 10.9, "Modelo de tres capas ArchiMate 3.2 evidenciando silos de datos y Shadow IT", 
            ha='center', va='center', fontsize=10, style='italic', color='#4A5568')

    # Capa de Negocio (Amarillo ArchiMate)
    r_neg = patches.FancyBboxPatch((0.5, 7.5), 10, 3.1, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#D69E2E", facecolor="#FEFCBF")
    ax.add_patch(r_neg)
    ax.text(0.8, 10.3, "CAPA DE NEGOCIO (Business Layer)", fontsize=11, fontweight='bold', color="#744210")
    
    # Procesos As-Is
    b_procs = ["Onboarding &\nCaptación Web", "Evaluación &\nScoring Batch", "Formalización\nOTP Simple", "Desembolso\nManual Banco", 
               "Cobranza &\nMora en Excel", "Reclamos v.\nCorreo Outlook"]
    for i, p in enumerate(b_procs):
        bx = 0.8 + (i % 3) * 3.2
        by = 8.8 if i < 3 else 7.7
        b_card = patches.FancyBboxPatch((bx, by), 2.9, 0.9, boxstyle="round,pad=0.08", linewidth=1, edgecolor="#B7791F", facecolor="#FFFFF0")
        ax.add_patch(b_card)
        ax.text(bx + 1.45, by + 0.45, p, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#744210")

    # Capa de Aplicación (Azul ArchiMate)
    r_app = patches.FancyBboxPatch((0.5, 3.8), 10, 3.4, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#3182CE", facecolor="#BEE3F8")
    ax.add_patch(r_app)
    ax.text(0.8, 6.9, "CAPA DE APLICACIÓN (Application Layer)", fontsize=11, fontweight='bold', color="#2B6CB0")

    apps = [("Portal Web / App Móvil", "Frontend React sin sync"), 
            ("Core Créditos Legado", "Node.js monolítico sin API Gw"),
            ("ERP Contable Concar", "Local, sync nocturno batch CSV"), 
            ("HC-01: Excel Ruteo Cobranza", "Shadow IT crítico (8 asesores)"),
            ("HC-04: Excel Scoring Manual", "Shadow IT en reevaluaciones"),
            ("HC-03: Excel Conciliación", "Shadow IT de tesorería y bancos")]
    for i, (app_n, app_d) in enumerate(apps):
        ax_pos = 0.8 + (i % 3) * 3.2
        ay_pos = 5.4 if i < 3 else 4.1
        is_excel = "HC-" in app_n
        app_card = patches.FancyBboxPatch((ax_pos, ay_pos), 2.9, 1.0, boxstyle="round,pad=0.08", 
                                          linewidth=1.2 if is_excel else 1, 
                                          edgecolor="#E53E3E" if is_excel else "#2B6CB0", 
                                          facecolor="#FFF5F5" if is_excel else "#EBF8FF")
        ax.add_patch(app_card)
        ax.text(ax_pos + 1.45, ay_pos + 0.65, app_n, ha='center', va='center', fontsize=8.5, fontweight='bold', 
                color="#C53030" if is_excel else "#2C5282")
        ax.text(ax_pos + 1.45, ay_pos + 0.28, app_d, ha='center', va='center', fontsize=7.2, color='#4A5568')

    # Capa de Tecnología (Verde ArchiMate)
    r_tec = patches.FancyBboxPatch((0.5, 0.5), 10, 3.0, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#38A169", facecolor="#C6F6D5")
    ax.add_patch(r_tec)
    ax.text(0.8, 3.2, "CAPA DE TECNOLOGÍA (Technology Layer)", fontsize=11, fontweight='bold', color="#22543D")

    tecs = [("AWS EC2 us-east-1", "Single-AZ, sin autoscaling"),
            ("RDS PostgreSQL 13", "Single-AZ, backups manuales"),
            ("Servidor On-Premise", "WinServer local (Contabilidad)"),
            ("LAN Sede Central", "Sin segmentación VLAN"),
            ("Dispositivos BYOD", "Móviles sin control MDM"),
            ("Internet 100 Mbps", "Enlace único sin failover")]
    for i, (t_n, t_d) in enumerate(tecs):
        tx_pos = 0.8 + (i % 3) * 3.2
        ty_pos = 1.9 if i < 3 else 0.8
        tec_card = patches.FancyBboxPatch((tx_pos, ty_pos), 2.9, 0.9, boxstyle="round,pad=0.08", linewidth=1, edgecolor="#2F855A", facecolor="#F0FFF4")
        ax.add_patch(tec_card)
        ax.text(tx_pos + 1.45, ty_pos + 0.55, t_n, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#22543D")
        ax.text(tx_pos + 1.45, ty_pos + 0.25, t_d, ha='center', va='center', fontsize=7.2, color='#4A5568')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12)

    plt.tight_layout()
    g4_path = os.path.join(out_dir, "AR_arquitectura_actual_asis.png")
    plt.savefig(g4_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 4 guardado en: {g4_path}")

    # -------------------------------------------------------------------------
    # Gráfico 5: Arquitectura Objetivo (To-Be) - 3 Capas
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(11, 8), facecolor='white')
    ax.set_facecolor("#FFFFFF")
    ax.axis('off')

    ax.text(5.5, 11.4, "ARQUITECTURA EMPRESARIAL OBJETIVO (TO-BE) · CREDITECH PERÚ", 
            ha='center', va='center', fontsize=14, fontweight='bold', color=c_primario)
    ax.text(5.5, 10.9, "Modelo To-Be alineado a la Visión 2028: APIs en tiempo real, MDM y Cloud Multi-AZ", 
            ha='center', va='center', fontsize=10, style='italic', color='#4A5568')

    # Capa de Negocio Objetivo
    r_neg_tb = patches.FancyBboxPatch((0.5, 7.5), 10, 3.1, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#D69E2E", facecolor="#FEFCBF")
    ax.add_patch(r_neg_tb)
    ax.text(0.8, 10.3, "CAPA DE NEGOCIO OBJETIVO (Business Layer)", fontsize=11, fontweight='bold', color="#744210")

    b_procs_tb = ["Autoservicio Digital\nOmnicanal 24/7", "Evaluación Asistida &\nScoring Explicable", "Firma PKI Acreditada\nPagaré Inmutable", 
                  "Desembolso Inmediato\nvía APIs Bancarias", "Cobranza Inteligente\nOmnicanal Segmentada", "Mesa Reclamos ITSM\nSLA SBS/INDECOPI"]
    for i, p in enumerate(b_procs_tb):
        bx = 0.8 + (i % 3) * 3.2
        by = 8.8 if i < 3 else 7.7
        b_card = patches.FancyBboxPatch((bx, by), 2.9, 0.9, boxstyle="round,pad=0.08", linewidth=1, edgecolor="#38A169", facecolor="#F0FFF4")
        ax.add_patch(b_card)
        ax.text(bx + 1.45, by + 0.45, p, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#22543D")

    # Capa de Aplicación Objetivo
    r_app_tb = patches.FancyBboxPatch((0.5, 3.8), 10, 3.4, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#3182CE", facecolor="#BEE3F8")
    ax.add_patch(r_app_tb)
    ax.text(0.8, 6.9, "CAPA DE APLICACIÓN OBJETIVO (Application Layer)", fontsize=11, fontweight='bold', color="#2B6CB0")

    apps_tb = [("Portal Web & App v2", "Autoservicio con biometría"), 
               ("API Gateway Corporativo", "Kong/AWS con OAuth 2.0 y mTLS"),
               ("Maestro Clientes MDM", "Fuente autoritativa gobernada"), 
               ("CRM/BPM de Cobranzas", "Sustituye 100% Shadow IT"),
               ("Motor Scoring API v2", "Microservicio con explicabilidad"),
               ("Sistema Helpdesk ITSM", "Integrado a SBS y defensas")]
    for i, (app_n, app_d) in enumerate(apps_tb):
        ax_pos = 0.8 + (i % 3) * 3.2
        ay_pos = 5.4 if i < 3 else 4.1
        app_card = patches.FancyBboxPatch((ax_pos, ay_pos), 2.9, 1.0, boxstyle="round,pad=0.08", 
                                          linewidth=1.2, edgecolor="#2B6CB0", facecolor="#EBF8FF")
        ax.add_patch(app_card)
        ax.text(ax_pos + 1.45, ay_pos + 0.65, app_n, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#2C5282")
        ax.text(ax_pos + 1.45, ay_pos + 0.28, app_d, ha='center', va='center', fontsize=7.2, color='#4A5568')

    # Capa de Tecnología Objetivo
    r_tec_tb = patches.FancyBboxPatch((0.5, 0.5), 10, 3.0, boxstyle="round,pad=0.1", linewidth=1.5, edgecolor="#38A169", facecolor="#C6F6D5")
    ax.add_patch(r_tec_tb)
    ax.text(0.8, 3.2, "CAPA DE TECNOLOGÍA OBJETIVO (Technology Layer)", fontsize=11, fontweight='bold', color="#22543D")

    tecs_tb = [("AWS EKS Contenedores", "Multi-AZ con autoescalado"),
               ("Aurora PostgreSQL Multi-AZ", "Failover <30s y DRP validado"),
               ("Bóveda WORM S3 Lock", "Inmutabilidad de pagarés y facturas"),
               ("SIEM Centralizado / SOC", "Monitoreo de seguridad 24/7"),
               ("Agentes MDM Móviles", "Cifrado en reposo en terminales"),
               ("SD-WAN y Enlace Redundante", "Continuidad de enlace 99.9%")]
    for i, (t_n, t_d) in enumerate(tecs_tb):
        tx_pos = 0.8 + (i % 3) * 3.2
        ty_pos = 1.9 if i < 3 else 0.8
        tec_card = patches.FancyBboxPatch((tx_pos, ty_pos), 2.9, 0.9, boxstyle="round,pad=0.08", linewidth=1, edgecolor="#2F855A", facecolor="#F0FFF4")
        ax.add_patch(tec_card)
        ax.text(tx_pos + 1.45, ty_pos + 0.55, t_n, ha='center', va='center', fontsize=8.5, fontweight='bold', color="#22543D")
        ax.text(tx_pos + 1.45, ty_pos + 0.25, t_d, ha='center', va='center', fontsize=7.2, color='#4A5568')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 12)

    plt.tight_layout()
    g5_path = os.path.join(out_dir, "AR_arquitectura_objetivo_tobe.png")
    plt.savefig(g5_path, dpi=300)
    plt.close()
    print(f"[OK] Gráfico 5 guardado en: {g5_path}")

if __name__ == "__main__":
    main()
