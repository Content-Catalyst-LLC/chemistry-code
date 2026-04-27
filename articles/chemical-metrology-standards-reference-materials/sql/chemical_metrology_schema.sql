DROP TABLE IF EXISTS uncertainty_budget;
DROP TABLE IF EXISTS reference_materials;
DROP TABLE IF EXISTS traceability_chain;
DROP TABLE IF EXISTS interlaboratory_comparison;
DROP TABLE IF EXISTS calibration_hierarchy;
DROP TABLE IF EXISTS provenance_artifacts;

CREATE TABLE uncertainty_budget (
    component TEXT PRIMARY KEY,
    standard_uncertainty REAL NOT NULL,
    unit TEXT NOT NULL,
    category TEXT NOT NULL,
    notes TEXT NOT NULL
);

CREATE TABLE reference_materials (
    material_id TEXT PRIMARY KEY,
    material_type TEXT NOT NULL,
    measurand TEXT NOT NULL,
    certified_value REAL NOT NULL,
    expanded_uncertainty REAL NOT NULL,
    unit TEXT NOT NULL,
    matrix TEXT NOT NULL,
    traceability_statement TEXT NOT NULL
);

CREATE TABLE traceability_chain (
    step_order INTEGER PRIMARY KEY,
    chain_level TEXT NOT NULL,
    artifact_or_process TEXT NOT NULL,
    reference TEXT NOT NULL,
    expanded_uncertainty REAL NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE interlaboratory_comparison (
    laboratory TEXT PRIMARY KEY,
    lab_result REAL NOT NULL,
    lab_expanded_uncertainty REAL NOT NULL,
    reference_value REAL NOT NULL,
    reference_expanded_uncertainty REAL NOT NULL,
    unit TEXT NOT NULL
);

CREATE TABLE calibration_hierarchy (
    level INTEGER PRIMARY KEY,
    description TEXT NOT NULL,
    example_artifact TEXT NOT NULL,
    documentation_required TEXT NOT NULL
);

CREATE TABLE provenance_artifacts (
    artifact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    artifact_name TEXT NOT NULL,
    artifact_type TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    checksum_sha256 TEXT,
    notes TEXT
);

INSERT INTO uncertainty_budget VALUES
('balance',0.004,'mg/L','calibration','Synthetic balance contribution'),
('volumetric_flask',0.006,'mg/L','volumetric','Synthetic volumetric contribution'),
('reference_material',0.010,'mg/L','reference','Synthetic CRM contribution'),
('calibration_curve',0.015,'mg/L','model','Synthetic calibration model contribution'),
('repeatability',0.012,'mg/L','precision','Synthetic repeatability contribution'),
('matrix_effect',0.020,'mg/L','matrix','Synthetic matrix effect contribution');

INSERT INTO reference_materials VALUES
('CRM_A','CRM','lead_mass_fraction',12.4,0.6,'mg/kg','soil','Traceable through certified reference value'),
('CRM_B','CRM','arsenic_mass_fraction',3.8,0.3,'mg/kg','rice','Traceable through certified reference value'),
('SRM_C','SRM','glucose_concentration',5.55,0.12,'mmol/L','serum','Traceable through standard reference material certificate'),
('RM_D','RM','nitrate_concentration',2.20,0.20,'mg/L','water','Reference value for quality control');

INSERT INTO traceability_chain VALUES
(1,'SI_reference','amount_of_substance_and_mass','SI_units',0.000,'mg/L'),
(2,'national_reference','national_metrology_institute_reference','NMI_reference_value',0.020,'mg/L'),
(3,'certified_reference_material','CRM_A_certificate','certified_value',0.060,'mg/L'),
(4,'laboratory_working_standard','prepared_working_standard','CRM_A',0.080,'mg/L'),
(5,'instrument_calibration','calibration_curve','working_standard_series',0.120,'mg/L'),
(6,'unknown_sample_result','reported_sample_value','calibrated_measurement_system',0.200,'mg/L');

INSERT INTO interlaboratory_comparison VALUES
('Lab_A',10.2,0.8,10.0,0.4,'mg/L'),
('Lab_B',9.7,0.7,10.0,0.4,'mg/L'),
('Lab_C',11.4,0.9,10.0,0.4,'mg/L'),
('Lab_D',8.9,1.0,10.0,0.4,'mg/L'),
('Lab_E',10.1,0.5,10.0,0.4,'mg/L');

INSERT INTO calibration_hierarchy VALUES
(1,'Primary or national reference','NMI reference value','reference certificate'),
(2,'Certified reference material','CRM certificate','certified value and uncertainty'),
(3,'Working standard','laboratory standard','preparation record'),
(4,'Calibration curve','instrument calibration','calibration model and residuals'),
(5,'Quality control material','QC sample','control chart record'),
(6,'Unknown sample','reported result','result uncertainty and provenance');

INSERT INTO provenance_artifacts (artifact_name, artifact_type, relative_path, checksum_sha256, notes) VALUES
('uncertainty_budget.csv','synthetic_data','data/uncertainty_budget.csv',NULL,'Synthetic uncertainty-budget data'),
('reference_materials.csv','synthetic_data','data/reference_materials.csv',NULL,'Synthetic reference-material records'),
('traceability_chain.csv','synthetic_data','data/traceability_chain.csv',NULL,'Synthetic traceability-chain metadata'),
('interlaboratory_comparison.csv','synthetic_data','data/interlaboratory_comparison.csv',NULL,'Synthetic interlaboratory comparison data'),
('calibration_hierarchy.csv','synthetic_data','data/calibration_hierarchy.csv',NULL,'Synthetic calibration hierarchy');
