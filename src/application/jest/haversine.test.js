import helpers from '../vue/helpers'

test('Correct distance is calculated', () => {
    expect(
        helpers.haversineDistance(
            -31.950402299750696,
            115.83429926800888,
            -32.0072775372602,
            115.89602146719497
        )
    ).toBe(8605.426676688201);
});
