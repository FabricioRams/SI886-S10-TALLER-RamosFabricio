import xml.etree.ElementTree as ET
import os

def create_archimate_model():
    root = ET.Element("archimate:model", {
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xmlns:archimate": "http://www.archimatetool.com/archimate",
        "name": "CrediTech Peru - Modelo de Arquitectura Empresarial (PETI 2026-2028)",
        "id": "id-creditech-arch-model",
        "version": "5.0.0"
    })

    # Folders
    f_strat = ET.SubElement(root, "folder", {"name": "Strategy", "id": "f-strat", "type": "strategy"})
    f_bus = ET.SubElement(root, "folder", {"name": "Business", "id": "f-bus", "type": "business"})
    f_app = ET.SubElement(root, "folder", {"name": "Application", "id": "f-app", "type": "application"})
    f_tec = ET.SubElement(root, "folder", {"name": "Technology & Physical", "id": "f-tec", "type": "technology"})
    f_mot = ET.SubElement(root, "folder", {"name": "Motivation", "id": "f-mot", "type": "motivation"})
    f_imp = ET.SubElement(root, "folder", {"name": "Implementation & Migration", "id": "f-imp", "type": "implementation_migration"})
    f_oth = ET.SubElement(root, "folder", {"name": "Other", "id": "f-oth", "type": "other"})
    f_rel = ET.SubElement(root, "folder", {"name": "Relations", "id": "f-rel", "type": "relations"})
    f_views = ET.SubElement(root, "folder", {"name": "Views", "id": "f-views", "type": "diagrams"})

    # Motivation: Principles
    principles = [
        ("elem-pr-01", "PR-01: Dato unico con fuente autoritativa y dueno designado"),
        ("elem-pr-02", "PR-02: Integracion desacoplada mediante APIs y servicios seguros"),
        ("elem-pr-03", "PR-03: Automatizacion end-to-end y erradicacion del Shadow IT"),
        ("elem-pr-04", "PR-04: Privacidad, seguridad y cumplimiento normativo por diseno"),
        ("elem-pr-05", "PR-05: Resiliencia, alta disponibilidad e inmutabilidad Cloud"),
        ("elem-pr-06", "PR-06: Autoservicio omnicanal con explicabilidad algoritmica")
    ]
    for p_id, p_name in principles:
        ET.SubElement(f_mot, "element", {"xsi:type": "archimate:Principle", "id": p_id, "name": p_name})

    # Business elements
    bus_actors = [
        ("elem-ba-cli", "Cliente / Solicitante de Microcredito"),
        ("elem-ba-ase", "Asesor Comercial Digital"),
        ("elem-ba-ana", "Analista de Creditos y Riesgos"),
        ("elem-ba-ges", "Gestor de Cobranzas"),
        ("elem-ba-fin", "Analista de Tesoreria"),
        ("elem-ba-cis", "Oficial de Cumplimiento / CISO")
    ]
    for a_id, a_name in bus_actors:
        ET.SubElement(f_bus, "element", {"xsi:type": "archimate:BusinessActor", "id": a_id, "name": a_name})

    bus_processes = [
        ("elem-bp-01", "Toma de Solicitud y Onboarding Digital"),
        ("elem-bp-02", "Evaluacion y Scoring de Riesgo Crediticio"),
        ("elem-bp-03", "Formalizacion Contractual y Pagare"),
        ("elem-bp-04", "Desembolso y Liquidacion de Fondos"),
        ("elem-bp-05", "Facturacion y Emision de Comprobantes"),
        ("elem-bp-06", "Ruteo y Cobranza Preventiva"),
        ("elem-bp-07", "Gestion de Mora Prejudicial"),
        ("elem-bp-08", "Atencion de Reclamos y Apelaciones"),
        ("elem-bp-09", "Conciliacion Bancaria y Tesoreria"),
        ("elem-bp-10", "Analisis Financiero y Riesgo de Cartera")
    ]
    for bp_id, bp_name in bus_processes:
        ET.SubElement(f_bus, "element", {"xsi:type": "archimate:BusinessProcess", "id": bp_id, "name": bp_name})

    bus_objects = [
        ("elem-bo-01", "Solicitud de Credito"),
        ("elem-bo-02", "Maestro de Clientes"),
        ("elem-bo-03", "Pagare y Contrato"),
        ("elem-bo-04", "Saldo y Amortizacion"),
        ("elem-bo-05", "Comprobante Electronico SUNAT"),
        ("elem-bo-06", "Cartera y Tramo de Mora")
    ]
    for bo_id, bo_name in bus_objects:
        ET.SubElement(f_bus, "element", {"xsi:type": "archimate:BusinessObject", "id": bo_id, "name": bo_name})

    # Application elements (As-Is & To-Be)
    app_comps = [
        ("elem-app-portal-asis", "Portal Web y App Movil v1 (As-Is)"),
        ("elem-app-core-asis", "Core de Creditos Legado Monolitico (As-Is)"),
        ("elem-app-erp-asis", "ERP Contable Concar Local (As-Is)"),
        ("elem-app-hc01", "HC-01: Hoja de Calculo Ruteo de Cobranzas (Shadow IT)"),
        ("elem-app-hc04", "HC-04: Hoja de Calculo Scoring Manual (Shadow IT)"),
        ("elem-app-hc03", "HC-03: Hoja de Calculo Conciliacion Bancaria (Shadow IT)"),
        ("elem-app-hc02", "HC-02: Hoja de Calculo Comercial y Prospectos (Shadow IT)"),
        ("elem-app-scoring-batch", "Motor Analitico de Scoring Scripts Batch (As-Is)"),
        ("elem-app-planillas", "Software de Planillas y RR.HH."),
        # To-Be
        ("elem-app-portal-tobe", "Portal Web y App Movil v2 Omnicanal (To-Be)"),
        ("elem-app-gw-tobe", "Capa de Integracion API Gateway Corporativo (To-Be)"),
        ("elem-app-mdm-tobe", "Servicio de Maestro de Clientes MDM (To-Be)"),
        ("elem-app-crm-tobe", "Plataforma CRM/BPM de Cobranzas (To-Be)"),
        ("elem-app-scoreapi-tobe", "Motor Scoring API v2 con Explicabilidad (To-Be)"),
        ("elem-app-itsm-tobe", "Mesa de Servicio ITSM y Reclamos Integrado (To-Be)"),
        ("elem-app-firmapki-tobe", "Modulo de Firma Digital PKI Acreditada IOFE (To-Be)")
    ]
    for comp_id, comp_name in app_comps:
        ET.SubElement(f_app, "element", {"xsi:type": "archimate:ApplicationComponent", "id": comp_id, "name": comp_name})

    # Technology elements
    tec_nodes = [
        ("elem-tec-onprem", "Servidor Local On-Premise Windows Server"),
        ("elem-tec-ec2", "Instancia AWS EC2 us-east-1 (Single-AZ)"),
        ("elem-tec-rds", "Amazon RDS PostgreSQL (Single-AZ)"),
        ("elem-tec-workstations", "Estaciones de Trabajo de Oficina (64 PCs)"),
        ("elem-tec-byod", "Dispositivos Moviles Personales BYOD"),
        # To-Be
        ("elem-tec-eks", "Cluster AWS EKS Contenedores (Multi-AZ)"),
        ("elem-tec-aurora", "Amazon Aurora PostgreSQL Serverless Multi-AZ"),
        ("elem-tec-worm", "Boveda Inmutable AWS S3 Object Lock (WORM)"),
        ("elem-tec-siem", "Plataforma SIEM Centralizada / SOC 24/7"),
        ("elem-tec-mdm", "Agentes de Seguridad Movil MDM Corporativo")
    ]
    for tn_id, tn_name in tec_nodes:
        ET.SubElement(f_tec, "element", {"xsi:type": "archimate:Node", "id": tn_id, "name": tn_name})

    # Implementation: Work Packages
    work_pkgs = [
        ("elem-wp-01", "PT-01: Gobierno del Dato y Maestro MDM"),
        ("elem-wp-02", "PT-02: Privacidad y Cumplimiento ANPD"),
        ("elem-wp-03", "PT-03: Firma Digital PKI y Boveda de Pagares"),
        ("elem-wp-04", "PT-04: Plataforma CRM/BPM Cobranzas y Retiro Shadow IT"),
        ("elem-wp-05", "PT-05: Mesa de Servicio ITSM y Reclamos SBS"),
        ("elem-wp-06", "PT-06: Modernizacion de Scoring API v2"),
        ("elem-wp-07", "PT-07: Capa de Integracion API Gateway"),
        ("elem-wp-08", "PT-08: Infraestructura Cloud Multi-AZ y DRP"),
        ("elem-wp-09", "PT-09: Monitoreo Centralizado SIEM/SOC 24/7")
    ]
    for wp_id, wp_name in work_pkgs:
        ET.SubElement(f_imp, "element", {"xsi:type": "archimate:WorkPackage", "id": wp_id, "name": wp_name})

    # Relations
    relations = [
        ("rel-01", "archimate:ServingRelationship", "elem-app-hc01", "elem-bp-06", "Soporta informalmente (Shadow IT)"),
        ("rel-02", "archimate:ServingRelationship", "elem-app-hc01", "elem-bp-07", "Soporta informalmente (Shadow IT)"),
        ("rel-03", "archimate:ServingRelationship", "elem-app-hc04", "elem-bp-02", "Reevaluacion manual en Excel"),
        ("rel-04", "archimate:ServingRelationship", "elem-app-hc03", "elem-bp-09", "Conciliacion manual en Excel"),
        ("rel-05", "archimate:ServingRelationship", "elem-app-crm-tobe", "elem-bp-06", "Soporte corporativo automatizado"),
        ("rel-06", "archimate:ServingRelationship", "elem-app-crm-tobe", "elem-bp-07", "Soporte corporativo automatizado"),
        ("rel-07", "archimate:ServingRelationship", "elem-app-scoreapi-tobe", "elem-bp-02", "Inferencia y explicabilidad API"),
        ("rel-08", "archimate:ServingRelationship", "elem-app-itsm-tobe", "elem-bp-08", "Tickets de atencion formal con SLA"),
        ("rel-09", "archimate:ServingRelationship", "elem-app-gw-tobe", "elem-app-crm-tobe", "Interconexion mTLS"),
        ("rel-10", "archimate:ServingRelationship", "elem-app-gw-tobe", "elem-app-scoreapi-tobe", "Publicacion y proxy de servicio"),
        ("rel-11", "archimate:RealizationRelationship", "elem-wp-04", "elem-app-crm-tobe", "Implementa"),
        ("rel-12", "archimate:RealizationRelationship", "elem-wp-01", "elem-app-mdm-tobe", "Implementa"),
        ("rel-13", "archimate:RealizationRelationship", "elem-wp-07", "elem-app-gw-tobe", "Implementa")
    ]
    for r_id, r_type, src, tgt, name in relations:
        ET.SubElement(f_rel, "element", {
            "xsi:type": r_type,
            "id": r_id,
            "source": src,
            "target": tgt,
            "name": name
        })

    # Views (Diagrams)
    v1 = ET.SubElement(f_views, "element", {
        "xsi:type": "archimate:ArchimateDiagramModel",
        "id": "view-cooperacion-proceso-app",
        "name": "Vista de Cooperacion Proceso-Aplicacion (As-Is)"
    })
    v2 = ET.SubElement(f_views, "element", {
        "xsi:type": "archimate:ArchimateDiagramModel",
        "id": "view-arquitectura-actual-asis",
        "name": "Arquitectura Empresarial Actual (As-Is)"
    })
    v3 = ET.SubElement(f_views, "element", {
        "xsi:type": "archimate:ArchimateDiagramModel",
        "id": "view-arquitectura-objetivo-tobe",
        "name": "Arquitectura Empresarial Objetivo (To-Be)"
    })

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    out_path = r"c:\PETI-2026-II\SI886-S10-TALLER-RamosFabricio\anexos\anexo_A_modelo_arquitectura.archimate"
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    print(f"Modelo ArchiMate exportado exitosamente en: {out_path}")

if __name__ == "__main__":
    create_archimate_model()
