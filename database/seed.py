from datetime import date
from sqlalchemy.orm import Session
from models import *


def seed():
    with Session(engine) as session:
 
        # ==========================
        # 1. Categorías
        # ==========================
        categorias = {
            "Inteligencia Artificial": Category(name="Inteligencia Artificial"),
            "Data Science": Category(name="Data Science"),
            "Ciberseguridad": Category(name="Ciberseguridad"),
            "Desarrollo Web": Category(name="Desarrollo Web"),
            "Programación Python": Category(name="Programación Python"),
            "Programación Java": Category(name="Programación Java"),
            "Bases de Datos": Category(name="Bases de Datos"),
            "Cloud Computing": Category(name="Cloud Computing"),
        }
        session.add_all(categorias.values())
        session.flush()  # asigna IDs
 
        # ==========================
        # 2. Instructores
        # ==========================
        instructores = [
            Instructor(first_name="Laura", last_name="Gómez", email="laura.gomez@edu.com",
                       specialty="Machine Learning", years_experience=9),
            Instructor(first_name="Carlos", last_name="Ramírez", email="carlos.ramirez@edu.com",
                       specialty="Deep Learning", years_experience=7),
            Instructor(first_name="Ana", last_name="Torres", email="ana.torres@edu.com",
                       specialty="Análisis de Datos", years_experience=6),
            Instructor(first_name="Diego", last_name="Fernández", email="diego.fernandez@edu.com",
                       specialty="Ciberseguridad Ofensiva", years_experience=10),
            Instructor(first_name="María", last_name="López", email="maria.lopez@edu.com",
                       specialty="Seguridad de Redes", years_experience=8),
            Instructor(first_name="Javier", last_name="Morales", email="javier.morales@edu.com",
                       specialty="Desarrollo Full Stack", years_experience=5),
            Instructor(first_name="Sofía", last_name="Castro", email="sofia.castro@edu.com",
                       specialty="Python Avanzado", years_experience=6),
            Instructor(first_name="Pedro", last_name="Sánchez", email="pedro.sanchez@edu.com",
                       specialty="Java Enterprise", years_experience=11),
            Instructor(first_name="Valentina", last_name="Rojas", email="valentina.rojas@edu.com",
                       specialty="Bases de Datos SQL", years_experience=7),
            Instructor(first_name="Andrés", last_name="Vargas", email="andres.vargas@edu.com",
                       specialty="Arquitectura Cloud (AWS/Azure)", years_experience=8),
        ]
        session.add_all(instructores)
        session.flush()
 
        (laura, carlos, ana, diego, maria,
         javier, sofia, pedro, valentina, andres) = instructores
 
        # ==========================
        # 3. Cursos (20)
        # ==========================
        cursos = [
            Course(name="Fundamentos de Inteligencia Artificial",
                   description="Introducción a los conceptos clave de la IA moderna.",
                   level="Básico", duration_hours=30, price=99.99, available_slots=40,
                   active=True, category=categorias["Inteligencia Artificial"],
                   instructors=[laura]),
            Course(name="Machine Learning Aplicado",
                   description="Algoritmos de aprendizaje supervisado y no supervisado.",
                   level="Intermedio", duration_hours=45, price=149.99, available_slots=35,
                   active=True, category=categorias["Inteligencia Artificial"],
                   instructors=[laura, carlos]),
            Course(name="Deep Learning con TensorFlow y PyTorch",
                   description="Redes neuronales profundas para visión y NLP.",
                   level="Avanzado", duration_hours=60, price=199.99, available_slots=25,
                   active=True, category=categorias["Inteligencia Artificial"],
                   instructors=[carlos]),
            Course(name="Procesamiento de Lenguaje Natural (NLP)",
                   description="Modelos de lenguaje, embeddings y transformers.",
                   level="Avanzado", duration_hours=50, price=179.99, available_slots=20,
                   active=True, category=categorias["Inteligencia Artificial"],
                   instructors=[carlos, laura]),
 
            Course(name="Introducción a Data Science",
                   description="Ciclo de vida de un proyecto de datos, de principio a fin.",
                   level="Básico", duration_hours=35, price=89.99, available_slots=50,
                   active=True, category=categorias["Data Science"],
                   instructors=[ana]),
            Course(name="Análisis y Visualización de Datos con Python",
                   description="Pandas, Matplotlib y Seaborn para explorar datos.",
                   level="Intermedio", duration_hours=40, price=119.99, available_slots=40,
                   active=True, category=categorias["Data Science"],
                   instructors=[ana, sofia]),
            Course(name="Estadística Aplicada para Ciencia de Datos",
                   description="Fundamentos estadísticos para modelos predictivos.",
                   level="Intermedio", duration_hours=38, price=109.99, available_slots=30,
                   active=True, category=categorias["Data Science"],
                   instructors=[ana]),
 
            Course(name="Fundamentos de Ciberseguridad",
                   description="Principios de seguridad informática y buenas prácticas.",
                   level="Básico", duration_hours=25, price=79.99, available_slots=45,
                   active=True, category=categorias["Ciberseguridad"],
                   instructors=[maria]),
            Course(name="Ethical Hacking y Pentesting",
                   description="Metodologías de pruebas de penetración en entornos reales.",
                   level="Avanzado", duration_hours=55, price=189.99, available_slots=20,
                   active=True, category=categorias["Ciberseguridad"],
                   instructors=[diego]),
            Course(name="Seguridad en Redes y Firewalls",
                   description="Protección perimetral, VPNs y monitoreo de tráfico.",
                   level="Intermedio", duration_hours=40, price=129.99, available_slots=30,
                   active=True, category=categorias["Ciberseguridad"],
                   instructors=[maria, diego]),
 
            Course(name="Desarrollo Web con HTML, CSS y JavaScript",
                   description="Bases del desarrollo frontend moderno.",
                   level="Básico", duration_hours=30, price=69.99, available_slots=60,
                   active=True, category=categorias["Desarrollo Web"],
                   instructors=[javier]),
            Course(name="Desarrollo Full Stack con React y Node.js",
                   description="Construcción de aplicaciones web completas.",
                   level="Avanzado", duration_hours=65, price=199.99, available_slots=25,
                   active=True, category=categorias["Desarrollo Web"],
                   instructors=[javier]),
 
            Course(name="Python desde Cero",
                   description="Sintaxis, estructuras de datos y lógica de programación.",
                   level="Básico", duration_hours=30, price=59.99, available_slots=70,
                   active=True, category=categorias["Programación Python"],
                   instructors=[sofia]),
            Course(name="Python Intermedio: POO y Buenas Prácticas",
                   description="Programación orientada a objetos y patrones de diseño.",
                   level="Intermedio", duration_hours=35, price=99.99, available_slots=45,
                   active=True, category=categorias["Programación Python"],
                   instructors=[sofia]),
            Course(name="Automatización con Python",
                   description="Scripts para automatizar tareas repetitivas y APIs.",
                   level="Intermedio", duration_hours=28, price=89.99, available_slots=40,
                   active=False, category=categorias["Programación Python"],
                   instructors=[sofia, ana]),
 
            Course(name="Java desde Cero",
                   description="Fundamentos del lenguaje Java y su ecosistema.",
                   level="Básico", duration_hours=32, price=64.99, available_slots=55,
                   active=True, category=categorias["Programación Java"],
                   instructors=[pedro]),
            Course(name="Java Enterprise con Spring Boot",
                   description="Desarrollo de APIs REST empresariales con Spring.",
                   level="Avanzado", duration_hours=55, price=179.99, available_slots=25,
                   active=True, category=categorias["Programación Java"],
                   instructors=[pedro]),
 
            Course(name="SQL desde Cero",
                   description="Consultas, joins y diseño de bases de datos relacionales.",
                   level="Básico", duration_hours=25, price=54.99, available_slots=60,
                   active=True, category=categorias["Bases de Datos"],
                   instructors=[valentina]),
            Course(name="Optimización de Bases de Datos y SQL Avanzado",
                   description="Índices, transacciones y tuning de rendimiento.",
                   level="Avanzado", duration_hours=40, price=139.99, available_slots=20,
                   active=True, category=categorias["Bases de Datos"],
                   instructors=[valentina, pedro]),
 
            Course(name="Fundamentos de Cloud Computing (AWS/Azure)",
                   description="Servicios en la nube, despliegue y escalabilidad.",
                   level="Intermedio", duration_hours=45, price=149.99, available_slots=30,
                   active=True, category=categorias["Cloud Computing"],
                   instructors=[andres]),
        ]
        session.add_all(cursos)
        session.flush()
 
        # ==========================
        # 4. Estudiantes (15)
        # ==========================
        estudiantes = [
            Student(first_name="Mateo", last_name="Pérez", email="mateo.perez@mail.com", scholarship=False),
            Student(first_name="Isabella", last_name="Díaz", email="isabella.diaz@mail.com", scholarship=True),
            Student(first_name="Santiago", last_name="Herrera", email="santiago.herrera@mail.com", scholarship=False),
            Student(first_name="Camila", last_name="Ortiz", email="camila.ortiz@mail.com", scholarship=False),
            Student(first_name="Sebastián", last_name="Ruiz", email="sebastian.ruiz@mail.com", scholarship=True),
            Student(first_name="Valeria", last_name="Molina", email="valeria.molina@mail.com", scholarship=False),
            Student(first_name="Nicolás", last_name="Cruz", email="nicolas.cruz@mail.com", scholarship=False),
            Student(first_name="Daniela", last_name="Reyes", email="daniela.reyes@mail.com", scholarship=True),
            Student(first_name="Emilio", last_name="Guzmán", email="emilio.guzman@mail.com", scholarship=False),
            Student(first_name="Renata", last_name="Navarro", email="renata.navarro@mail.com", scholarship=False),
            Student(first_name="Tomás", last_name="Salazar", email="tomas.salazar@mail.com", scholarship=True),
            Student(first_name="Antonia", last_name="Campos", email="antonia.campos@mail.com", scholarship=False),
            Student(first_name="Joaquín", last_name="Peña", email="joaquin.pena@mail.com", scholarship=False),
            Student(first_name="Florencia", last_name="Silva", email="florencia.silva@mail.com", scholarship=True),
            Student(first_name="Benjamín", last_name="Contreras", email="benjamin.contreras@mail.com", scholarship=False),
        ]
        session.add_all(estudiantes)
        session.flush()
 
        (mateo, isabella, santiago, camila, sebastian,
         valeria, nicolas, daniela, emilio, renata,
         tomas, antonia, joaquin, florencia, benjamin) = estudiantes
 
        # ==========================
        # 5. Inscripciones (25)
        # ==========================
        c = cursos  # alias corto por índice (orden de creación arriba, 0-based)
        inscripciones = [
            Enrollment(student=mateo, course=c[1], enrollment_date=date(2025, 2, 10), status="Completado", progress=100.0),
            Enrollment(student=mateo, course=c[12], enrollment_date=date(2025, 5, 3), status="En progreso", progress=60.0),
            Enrollment(student=isabella, course=c[4], enrollment_date=date(2025, 1, 15), status="Completado", progress=100.0),
            Enrollment(student=isabella, course=c[5], enrollment_date=date(2025, 3, 20), status="En progreso", progress=45.0),
            Enrollment(student=santiago, course=c[7], enrollment_date=date(2025, 2, 1), status="Completado", progress=100.0),
            Enrollment(student=santiago, course=c[8], enrollment_date=date(2025, 4, 12), status="En progreso", progress=30.0),
            Enrollment(student=camila, course=c[10], enrollment_date=date(2025, 1, 8), status="Completado", progress=100.0),
            Enrollment(student=camila, course=c[11], enrollment_date=date(2025, 5, 18), status="Activo", progress=15.0),
            Enrollment(student=sebastian, course=c[12], enrollment_date=date(2025, 2, 22), status="Completado", progress=100.0),
            Enrollment(student=sebastian, course=c[13], enrollment_date=date(2025, 4, 2), status="En progreso", progress=70.0),
            Enrollment(student=valeria, course=c[15], enrollment_date=date(2025, 1, 30), status="Completado", progress=100.0),
            Enrollment(student=valeria, course=c[16], enrollment_date=date(2025, 6, 5), status="Activo", progress=10.0),
            Enrollment(student=nicolas, course=c[17], enrollment_date=date(2025, 3, 1), status="Completado", progress=100.0),
            Enrollment(student=nicolas, course=c[18], enrollment_date=date(2025, 5, 25), status="En progreso", progress=55.0),
            Enrollment(student=daniela, course=c[0], enrollment_date=date(2025, 1, 20), status="Completado", progress=100.0),
            Enrollment(student=daniela, course=c[3], enrollment_date=date(2025, 4, 10), status="En progreso", progress=40.0),
            Enrollment(student=emilio, course=c[19], enrollment_date=date(2025, 2, 14), status="Completado", progress=100.0),
            Enrollment(student=emilio, course=c[9], enrollment_date=date(2025, 6, 1), status="Activo", progress=5.0),
            Enrollment(student=renata, course=c[2], enrollment_date=date(2025, 3, 8), status="En progreso", progress=80.0),
            Enrollment(student=tomas, course=c[6], enrollment_date=date(2025, 2, 28), status="Completado", progress=100.0),
            Enrollment(student=antonia, course=c[1], enrollment_date=date(2025, 5, 30), status="Cancelado", progress=20.0),
            Enrollment(student=joaquin, course=c[14], enrollment_date=date(2025, 1, 5), status="Completado", progress=100.0),
            Enrollment(student=florencia, course=c[16], enrollment_date=date(2025, 3, 15), status="Completado", progress=100.0),
            Enrollment(student=benjamin, course=c[8], enrollment_date=date(2025, 4, 20), status="En progreso", progress=50.0),
            Enrollment(student=benjamin, course=c[17], enrollment_date=date(2025, 6, 10), status="Activo", progress=12.0),
        ]
        session.add_all(inscripciones)
        session.flush()
 
        # ==========================
        # 6. Certificados (10)
        # Emitidos solo para inscripciones "Completado"
        # ==========================
        certificados = [
            Certificate(student=mateo, course_name=c[1].name, issue_date=date(2025, 2, 12),
                        verification_code="CERT-2025-0001"),
            Certificate(student=isabella, course_name=c[4].name, issue_date=date(2025, 1, 18),
                        verification_code="CERT-2025-0002"),
            Certificate(student=santiago, course_name=c[7].name, issue_date=date(2025, 2, 3),
                        verification_code="CERT-2025-0003"),
            Certificate(student=camila, course_name=c[10].name, issue_date=date(2025, 1, 10),
                        verification_code="CERT-2025-0004"),
            Certificate(student=sebastian, course_name=c[12].name, issue_date=date(2025, 2, 25),
                        verification_code="CERT-2025-0005"),
            Certificate(student=valeria, course_name=c[15].name, issue_date=date(2025, 2, 2),
                        verification_code="CERT-2025-0006"),
            Certificate(student=nicolas, course_name=c[17].name, issue_date=date(2025, 3, 4),
                        verification_code="CERT-2025-0007"),
            Certificate(student=daniela, course_name=c[0].name, issue_date=date(2025, 1, 22),
                        verification_code="CERT-2025-0008"),
            Certificate(student=emilio, course_name=c[19].name, issue_date=date(2025, 2, 16),
                        verification_code="CERT-2025-0009"),
            Certificate(student=tomas, course_name=c[6].name, issue_date=date(2025, 3, 2),
                        verification_code="CERT-2025-0010"),
        ]
        session.add_all(certificados)
 
        session.commit()
        print("✅ Datos de prueba insertados correctamente:")
        print(f"   - {len(categorias)} categorías")
        print(f"   - {len(instructores)} instructores")
        print(f"   - {len(cursos)} cursos")
        print(f"   - {len(estudiantes)} estudiantes")
        print(f"   - {len(inscripciones)} inscripciones")
        print(f"   - {len(certificados)} certificados")