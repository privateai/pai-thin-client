from .base_processor import BaseProcessor


class SyntheticReplacementProcessor(BaseProcessor):
    def __call__(self, entity: dict) -> str:
        if "synthetic_text" not in entity:
            entity_type = entity["best_label"]
            raise ValueError(
                f"Entity '{entity.get('text', '')}' of type '{entity_type}' does not have a "
                f"`synthetic_text` field. Ensure that '{entity_type}' is enabled "
                "in synthetic_replacements.entity_types."
            )
        return entity["synthetic_text"]
