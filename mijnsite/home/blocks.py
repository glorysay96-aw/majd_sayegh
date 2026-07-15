from wagtail import blocks


class QuizQuestionBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True)

    answer_a = blocks.CharBlock(required=True)
    answer_b = blocks.CharBlock(required=True)
    answer_c = blocks.CharBlock(required=True)
    answer_d = blocks.CharBlock(required=True)

    correct_answer = blocks.ChoiceBlock(
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
        ]
    )

    explanation = blocks.TextBlock(required=False)

    class Meta:
        icon = "help"
        label = "Quizvraag"