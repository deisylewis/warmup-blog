# DnD Photos - Wedding Photography Website

A modern, elegant wedding photography website inspired by Alicia Wiley Photography's design, built with your DnD Photos content and branding.

## 🌟 Features

- **Modern Design**: Clean, elegant layout inspired by high-end photography websites
- **Responsive**: Fully responsive design that works on all devices
- **Interactive**: Smooth animations, lightbox gallery, and interactive elements
- **SEO Friendly**: Semantic HTML structure with proper meta tags
- **Fast Loading**: Optimized images and lazy loading
- **Contact Form**: Functional contact form with validation
- **Portfolio Gallery**: Clickable portfolio with lightbox view
- **Package Pricing**: Clear pricing structure for wedding packages

## 🚀 How to View the Website

### Method 1: Local Server (Recommended)
The website is currently running on a local server. You can view it by:

1. Open your web browser
2. Navigate to: `http://localhost:8000`

### Method 2: Direct File Opening
You can also open the `index.html` file directly in your browser, though some features may not work properly without a server.

## 📁 File Structure

```
/
├── index.html          # Main HTML file
├── styles.css          # CSS styling
├── script.js           # JavaScript functionality
└── README.md          # This file
```

## 🎨 Customization Guide

### 1. Content Updates

**Update Business Information:**
- Edit contact details in the contact section of `index.html`
- Update the hero title and subtitle
- Modify the about section with your story

**Update Pricing:**
- Edit the packages section in `index.html`
- Modify pricing in the package cards
- Update service descriptions

### 2. Images

**Replace Placeholder Images:**
The website currently uses Unsplash placeholder images. Replace them with your actual photos:

1. Create an `images` folder
2. Add your photos to this folder
3. Update image sources in `index.html`:
   ```html
   <!-- Replace this -->
   <img src="https://images.unsplash.com/..." alt="..." />
   
   <!-- With this -->
   <img src="images/your-photo.jpg" alt="..." />
   ```

**Recommended Image Sizes:**
- Hero image: 2000x1200px
- Portfolio images: 800x600px
- About image: 800x600px

### 3. Colors and Styling

**Update Brand Colors:**
Edit `styles.css` to change the color scheme:

```css
/* Primary colors */
:root {
    --primary-color: #000;      /* Black */
    --secondary-color: #666;    /* Gray */
    --accent-color: #f8f8f8;    /* Light gray */
    --text-color: #333;         /* Dark gray */
}
```

**Update Fonts:**
The website uses Playfair Display and Inter fonts. To change:

1. Update the Google Fonts link in `index.html`
2. Update font-family references in `styles.css`

### 4. Contact Form

**Email Integration:**
The contact form currently shows success/error messages. To make it functional:

1. Add a backend service (PHP, Node.js, etc.)
2. Or integrate with services like Formspree, Netlify Forms, or EmailJS
3. Update the form action in `index.html`

**Example with Formspree:**
```html
<form class="contact-form" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

## 🌐 Deployment Options

### 1. GitHub Pages (Free)
1. Create a GitHub repository
2. Upload your files
3. Enable GitHub Pages in repository settings
4. Your site will be available at `https://username.github.io/repository-name`

### 2. Netlify (Free)
1. Create account at netlify.com
2. Drag and drop your project folder
3. Get instant deployment with custom domain options

### 3. Vercel (Free)
1. Create account at vercel.com
2. Connect your GitHub repository
3. Automatic deployments on every push

### 4. Traditional Web Hosting
Upload files to any web hosting service via FTP/SFTP.

## 📱 Mobile Optimization

The website is fully responsive with breakpoints at:
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 320px - 767px

## 🔧 Technical Details

**Built With:**
- HTML5
- CSS3 (Flexbox, Grid, Custom Properties)
- Vanilla JavaScript (ES6+)
- Font Awesome icons
- Google Fonts

**Browser Support:**
- Chrome 70+
- Firefox 65+
- Safari 12+
- Edge 79+

## 📈 SEO Optimization

**Included SEO Features:**
- Semantic HTML structure
- Meta descriptions and titles
- Alt tags for images
- Schema markup ready
- Fast loading times

**To Improve SEO:**
1. Add meta descriptions to `<head>`
2. Create XML sitemap
3. Add Google Analytics
4. Optimize images further
5. Add schema markup for business information

## 🎯 Performance Tips

1. **Optimize Images:**
   - Use WebP format when possible
   - Compress images before upload
   - Use appropriate sizes for different devices

2. **Minimize Files:**
   - Minify CSS and JavaScript for production
   - Use a build tool like Vite or Webpack

3. **CDN Usage:**
   - Consider using a CDN for faster global loading
   - Optimize font loading

## 🐛 Troubleshooting

**Common Issues:**

1. **Images not loading:**
   - Check file paths
   - Ensure images are in correct folder
   - Verify image file extensions

2. **Contact form not working:**
   - Add backend service
   - Check form validation
   - Verify form action URL

3. **Mobile menu not working:**
   - Ensure JavaScript is loaded
   - Check for console errors
   - Verify mobile breakpoints

## 📞 Support

For customization help or technical support:
- Check browser console for errors
- Validate HTML and CSS
- Test on different devices and browsers

## 📄 License

This website template is created specifically for DnD Photos. Feel free to modify and use for your business needs.

---

**Built with ❤️ for DnD Photos**

*Last updated: January 2025*