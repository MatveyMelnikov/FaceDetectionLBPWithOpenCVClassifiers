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


def apply_scale(rect, scale):
    return Rectangle(
        (int(rect.pos[0] * scale),
         int(rect.pos[1] * scale)),
        (int(rect.size[0] * scale),
         int(rect.size[1] * scale))
    )


def apply_offset(rect, offset):
    return Rectangle(
        (rect.pos[0] + offset[0], rect.pos[1] + offset[1]),
        rect.size
    )


class HaarLikeFeature:
    # 1. rectangle from XML, 2. subset of masks, 3. float, 4. float
    def __init__(self, top_left_rect, masks, left_value, right_value):
        # self.rect = rect
        self.rects = None
        self.scaled_features = None
        self.masks = masks
        self.left_value = left_value
        self.right_value = right_value

        self.generate_lbp_rects(top_left_rect)

    def calculate_scaled_features(self, scales):
        self.scaled_features = []

        for scale in scales:
            scaled_rects = []

            for rect in self.rects:
                scaled_rects.append(apply_scale(rect, scale))

            self.scaled_features.append(scaled_rects)

    def generate_lbp_rects(self, top_left_rect):
        #  0  1  2  3
        #  4  5  6  7
        #  8  9 10 11
        # 12 13 14 15

        # Bits in LBP
        # *-*-*-*
        # |7|6|5|
        # *-*-*-*
        # |0| |4|
        # *-*-*-*
        # |1|2|3|
        # *-*-*-*

        self.rects = []

        for i in range(0, 3):
            create_lbp_rect_line_with_offset(self.rects, top_left_rect, top_left_rect.size[1] * i)

    def get_score(self, integral_image, offset, scale_index):
        score = 0

        # center_rect_with_offset = apply_offset_and_scale(self.rects[4], offset, scale)
        # center_value = IntegralImage.sum_region(
        #     integral_image,
        #     center_rect_with_offset
        # )
        #
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[0], offset, scale)
        # ) >= center_value:
        #     score |= 128
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[1], offset, scale)
        # ) >= center_value:
        #     score |= 64
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[2], offset, scale)
        # ) >= center_value:
        #     score |= 32
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[3], offset, scale)
        # ) >= center_value:
        #     score |= 1
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[5], offset, scale)
        # ) >= center_value:
        #     score |= 16
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[6], offset, scale)
        # ) >= center_value:
        #     score |= 2
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[7], offset, scale)
        # ) >= center_value:
        #     score |= 4
        # if IntegralImage.sum_region(
        #         integral_image,
        #         apply_offset_and_scale(self.rects[8], offset, scale)
        # ) >= center_value:
        #     score |= 8

        current_scale_rects = self.scaled_features[scale_index]

        center_rect_with_offset = apply_offset(current_scale_rects[4], offset)
        center_value = IntegralImage.sum_region(
            integral_image,
            center_rect_with_offset
        )

        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[0], offset)
        ) >= center_value:
            score |= 128
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[1], offset)
        ) >= center_value:
            score |= 64
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[2], offset)
        ) >= center_value:
            score |= 32
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[3], offset)
        ) >= center_value:
            score |= 1
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[5], offset)
        ) >= center_value:
            score |= 16
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[6], offset)
        ) >= center_value:
            score |= 2
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[7], offset)
        ) >= center_value:
            score |= 4
        if IntegralImage.sum_region(
                integral_image,
                apply_offset(current_scale_rects[8], offset)
        ) >= center_value:
            score |= 8

        return score

    # def calculate_rect_region_sum(self, integral_image, rect, value, center_value, offset, scale):
    #     if IntegralImage.sum_region(
    #             integral_image,
    #             apply_offset_and_scale(rect, offset, scale)
    #     ) >= center_value:
    #         return value
    #     return 0

    def get_vote(self, integral_image, offset, scale_index):
        score = self.get_score(integral_image, offset, scale_index)

        return self.right_value if self.masks[score >> 5] & (1 << (score & 31)) else self.left_value
