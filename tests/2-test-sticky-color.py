import pytest
from libtodolist import Task, TaskList, PriorityLevel, TaskColor

"""Spécifications:

On veut ajouter des couleurs aux tâches, pour les afficher par exemple comme des post-it

6 couleurs sont définies: YELLOW, BLUE, GREEN, PINK, ORANGE, PURPLE.

La couleur devra être un attribut .color des objets Task
Les couleurs possibles seront listées dans un Enum python nommé TaskColor situé dans la bibliothèque libtodolist (s'inspirer de PriorityLevel par exemple)

Les tâches ont des couleurs par défaut:
- Basse priorité: YELLOW
- Priorité normale: GREEN
- Priorité élevée: RED

Exercice 3: ajouter ces fonctionnalités à la bibliothèque. Faire un commit Git descriptif de ce qui a été fait.
Exercice 4: ajouter le rendu des couleurs à l'application Web (les classes CSS sont déjà proposées). Faire un commit Git descriptif.
Exercice 5: permettre dans le formulaire de création sur l'application Web de choisir la couleur lors de la création. Produire le test Selenium puis le code. Faire un commit Git.
Exercice 6: produire une critique constructive des tests unitaires que je vous propose.

Si l'exercice était noté la qualité du message de commit ferait partie de la notation car la clarté est importante dans un historique de code.
"""

def test_sticky_colors():
    """Check that all the sticky notes colors exist"""
    colors = [c.value for c in TaskColor]
    wanted_colors = ('YELLOW', 'BLUE', 'GREEN', 'PINK', 'ORANGE', 'PURPLE')
    assert all(c in colors for c in wanted_colors)
    
def test_default_colors():
    """A Task with priority LOW must be yellow by default"""
    t = Task(name="Test couleur par défaut/LOW", priority=PriorityLevel.LOW)
    assert t.color == TaskColor.YELLOW
    """A task with priority NORMAL must be green by default"""
    t2 = Task(name="Test couleur par défaut/NOR", priority=PriorityLevel.NORMAL)
    assert t.color == TaskColor.GREEN
    """A task with priority URGENT must be red by default"""
    t2 = Task(name="Test couleur par défaut/URG", priority=PriorityLevel.URGENT)
    assert t.color == TaskColor.RED
    
def test_color_custom():
    """You can create a task with a color directly"""
    t = Task(name="Test couleur dans constructeur", color=TaskColor.PINK)
    assert t.color == TaskColor.PINK
    """You can create a task and then assign a color to it"""
    t2 = Task(name="Test couleur a posteriori")
    t2.color = TaskColor.ORANGE
    assert t2.color == TaskColor.ORANGE

def test_color_persistence_in_file():
    t = Task(name="Test couleur persistée", color=TaskColor.PINK)
    tl = TaskList([t])
    tl.to_json('tmp.json')
    tl2 = TaskList.from_json('tmp.json')
    t2 = tl2.tasks[0]
    """Check that after saving we have the same color as before"""
    assert t.color == t2.color == TaskColor.PINK
    """Update the original object"""
    t.color = TaskColor.ORANGE
    """Assert the new object has not changed"""
    assert t2.color == TaskColor.PINK
    """Assert the new object has changed"""
    assert t.color == TaskColor.ORANGE
    """Save the new object and test equality again"""
    tl.to_json('tmp.json')
    tl2 = TaskList.from_json('tmp.json')
    t2 = tl2.tasks[0]
    assert t2.color == t.color