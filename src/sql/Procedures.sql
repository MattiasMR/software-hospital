DELIMITER $$

-- SP: Obtener estado de todos los boxes con filtros
CREATE PROCEDURE sp_get_box_status(
  IN p_corridor VARCHAR(50),
  IN p_specialty VARCHAR(100),
  IN p_status ENUM('Free','Occupied','Disabled'),
  IN p_doctor VARCHAR(150)
)
BEGIN
  SELECT 
    b.id, b.corridor, b.specialty, b.status,
    a.doctor_name, a.start_time, a.end_time
  FROM boxes b
  LEFT JOIN availability a 
    ON b.id = a.box_id 
    AND NOW() BETWEEN a.start_time AND a.end_time
  WHERE (p_corridor IS NULL OR b.corridor = p_corridor)
    AND (p_specialty IS NULL OR b.specialty = p_specialty)
    AND (p_status IS NULL OR b.status = p_status)
    AND (p_doctor IS NULL OR a.doctor_name = p_doctor);
END$$

-- SP: Obtener detalle de un box y su historial 7 días
CREATE PROCEDURE sp_get_box_detail(IN p_box_id INT)
BEGIN
  SELECT * 
  FROM boxes 
  WHERE id = p_box_id;

  SELECT doctor_name, start_time, end_time
  FROM availability
  WHERE box_id = p_box_id 
    AND start_time >= NOW() - INTERVAL 7 DAY;
END$$

-- SP: Generar reporte de horas ocupadas por box en un rango
CREATE PROCEDURE sp_get_occupancy_report(
  IN p_start_date DATETIME,
  IN p_end_date DATETIME
)
BEGIN
  SELECT 
    b.id AS box_id,
    SUM(
      TIMESTAMPDIFF(
        SECOND,
        GREATEST(a.start_time, p_start_date),
        LEAST(a.end_time, p_end_date)
      )
    )/3600 AS hours_occupied
  FROM boxes b
  LEFT JOIN availability a 
    ON b.id = a.box_id
    AND a.end_time >= p_start_date 
    AND a.start_time <= p_end_date
  GROUP BY b.id;
END$$

DELIMITER ;
