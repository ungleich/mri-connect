"""
Utility functions
"""

def expertiseByTopic(expertise):
    topics = {}
    for exp in expertise:
        if not exp.topic.id in topics:
            topics[exp.topic.id] = {
                'id': exp.topic.id,
                'title': exp.topic.title,
                'expertise': []
            }
        topics[exp.topic.id]['expertise'].append({
            'id': exp.id,
            'title': exp.title,
        })
    return [ v for k,v in topics.items() ]
