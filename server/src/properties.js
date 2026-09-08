export const supportedDestination = 'Asheville';

export const properties = [
  {
    id: 'blue-ridge-lodge',
    name: 'Blue Ridge Lodge',
    city: 'Asheville, North Carolina',
    rating: 4.7,
    reviewCount: 312,
    nightlyRate: 145,
    refundable: true,
    amenities: ['Mountain views', 'Breakfast included', 'Free parking'],
    imageTone: 'ridge',
    description: 'A calm base near the Blue Ridge Parkway.',
  },
  {
    id: 'river-arts-inn',
    name: 'River Arts Inn',
    city: 'Asheville, North Carolina',
    rating: 4.5,
    reviewCount: 198,
    nightlyRate: 118,
    refundable: true,
    amenities: ['Walkable district', 'Coffee bar', 'Pet friendly'],
    imageTone: 'river',
    description: 'A bright, creative stay close to local galleries.',
  },
  {
    id: 'chestnut-house',
    name: 'Chestnut House Hotel',
    city: 'Asheville, North Carolina',
    rating: 4.8,
    reviewCount: 421,
    nightlyRate: 182,
    refundable: false,
    amenities: ['Downtown', 'Rooftop terrace', 'Fitness room'],
    imageTone: 'chestnut',
    description: 'A polished downtown retreat with thoughtful details.',
  },
];

export function findProperty(propertyId) {
  return properties.find((property) => property.id === propertyId);
}

