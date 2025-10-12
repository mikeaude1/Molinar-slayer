from django.db import migrations


def seed_practice_areas(apps, schema_editor):
    PracticeArea = apps.get_model('practiceareas', 'PracticeArea')
    areas = [
        {"name": "Derecho Civil", "slug": "derechocivil"},
        {"name": "Derecho Penal", "slug": "derechopenal"},
        {"name": "Derecho Familiar", "slug": "derechofamiliar"},
        {"name": "Derecho Mercantil/Corporativo", "slug": "derechomercantil"},
        {"name": "Derecho Laboral", "slug": "derecholaboral"},
        {"name": "Derecho Fiscal", "slug": "derechofiscal"},
    ]

    for area in areas:
        obj, created = PracticeArea.objects.get_or_create(
            slug=area["slug"],
            defaults={
                "name": area["name"],
                "description": "",
                "active": True,
            },
        )
        if not created:
            # Asegurar que esté activa si ya existe
            if obj.active is False:
                obj.active = True
                obj.save(update_fields=["active"]) 


def unseed_practice_areas(apps, schema_editor):
    PracticeArea = apps.get_model('practiceareas', 'PracticeArea')
    slugs = [
        "derechocivil",
        "derechopenal",
        "derechofamiliar",
        "derechomercantil",
        "derecholaboral",
        "derechofiscal",
    ]
    PracticeArea.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("practiceareas", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_practice_areas, reverse_code=unseed_practice_areas),
    ]