import IntegralImage as IntegralImage

from Rectangle import Rectangle


def create_lbp_rect_line_with_offset(rects, top_left_rect, y_offset):
    rects.append(
        create_lbp_rect_with_offset(
            top_left_rect,
            (0, y_offset)
        )
    )
    for i in range(1, 3):
        rects.append(
            create_lbp_rect_with_offset(
                top_left_rect, (top_left_rect.size[0] * i, y_offset)
            )
        )


def create_lbp_rect_with_offset(base_rect, pos_offset):
    return Rectangle(
        (base_rect.pos[0] + pos_offset[0], base_rect.pos[1] + pos_offset[1]),
        base_rect.size
    )


def apply_offset_and_scale(rect, offset, scale):
    return Rectangle(
        (int(rect.pos[0] * scale + offset[0]),
         int(rect.pos[1] * scale + offset[1])),
        (int(rect.size[0] * scale),
         int(rect.size[1] * scale))
    )


class HaarLikeFeature:
    # 1. rectangle from XML, 2. subset of masks, 3. float, 4. float
    def __init__(self, top_left_rect, masks, left_value, right_value):
        # self.rect = rect
        self.rects = None
        self.masks = masks
        self.left_value = left_value
        self.right_value = right_value

        self.generate_lbp_rects(top_left_rect)

    def generate_lbp_rects(self, top_left_rect):
        #  0  1  2  3
        #  4  5  6  7
        #  8  9 10 11
        # 12 13 14 15

        self.rects = []

        for i in range(0, 3):
            create_lbp_rect_line_with_offset(self.rects, top_left_rect, top_left_rect.size[1] * i)

    def get_score(self, integral_image, offset, scale):
        score = 0

        center_rect_with_offset = apply_offset_and_scale(self.rects[4], offset, scale)
        center_value = IntegralImage.sum_region(
            integral_image,
            center_rect_with_offset
        )

        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[0], offset, scale)
        ) >= center_value:
            score |= 128
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[1], offset, scale)
        ) >= center_value:
            score |= 64
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[2], offset, scale)
        ) >= center_value:
            score |= 32
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[3], offset, scale)
        ) >= center_value:
            score |= 1
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[5], offset, scale)
        ) >= center_value:
            score |= 16
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[6], offset, scale)
        ) >= center_value:
            score |= 2
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[7], offset, scale)
        ) >= center_value:
            score |= 4
        if IntegralImage.sum_region(
                integral_image,
                apply_offset_and_scale(self.rects[8], offset, scale)
        ) >= center_value:
            score |= 8

        return score

    def get_vote(self, integral_image, offset, scale):
        score = self.get_score(integral_image, offset, scale)

        return self.right_value if self.masks[score >> 5] & (1 << (score & 31)) else self.left_value
